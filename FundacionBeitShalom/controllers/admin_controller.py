import math
from datetime import datetime
from functools import wraps

from flask import (Blueprint, render_template, request, flash, redirect,
                   url_for, session, send_file, abort)
from werkzeug.security import check_password_hash, generate_password_hash

from database import ErrorBaseDatos
from models.colaborador import (Colaborador, ESTADOS, PAISES,
                                MODALIDADES, DISPONIBILIDADES)
from repositories.administrador_repository import AdministradorRepository
from repositories.colaborador_repository import (ColaboradorRepository,
                                                 CorreoDuplicadoError)
from repositories.panel_repository import PanelRepository
from servicios.exportador_excel import crear_excel

# Esto sirve para: agrupar todas las rutas del panel bajo /admin
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
admins = AdministradorRepository()
panel = PanelRepository()
colaboradores = ColaboradorRepository()

# Esto sirve para: definir cuántas solicitudes se muestran por página
POR_PAGINA = 15
# Se compara contra este hash cuando el usuario no existe, para que tarde lo mismo
# Esto sirve para: que el login tarde igual si el usuario no existe (evita adivinar usuarios)
_HASH_FALSO = generate_password_hash("contraseña-falsa")


# Esto sirve para: bloquear rutas a quien no ha iniciado sesión
def admin_requerido(vista):
    """Autorización: solo deja pasar a quien inició sesión."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Inicia sesión para entrar al panel.", "info")
            return redirect(url_for("admin.login"))
        return vista(*args, **kwargs)
    return envoltura


# Esto sirve para: evitar que el navegador guarde páginas del panel en caché
@admin_bp.after_request
def sin_cache(respuesta):
    respuesta.headers["Cache-Control"] = "no-store"   # el botón "atrás" no muestra datos
    return respuesta


# Esto sirve para: mostrar una página de error si falla la base de datos
@admin_bp.errorhandler(ErrorBaseDatos)
def error_base_datos(error):
    return render_template("admin/error.html"), 503


# ---------- Acceso ----------
# Esto sirve para: iniciar sesión: valida usuario y contraseña y abre la sesión
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")
        admin = admins.obtener_por_usuario(usuario) if usuario else None

        if admin and admin.verificar_password(password):
            session.clear()                      # sesión nueva al entrar
            session["admin_id"] = admin.id
            session["admin_nombre"] = str(admin)
            session.permanent = True
            return redirect(url_for("admin.dashboard"))

        if not admin:
            check_password_hash(_HASH_FALSO, password)
        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("admin/login.html")


# Esto sirve para: cerrar sesión
@admin_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Cerraste sesión.", "info")
    return redirect(url_for("admin.login"))


# ---------- R: Leer ----------
# Esto sirve para: mostrar el dashboard con las estadísticas
@admin_bp.route("/")
@admin_requerido
def dashboard():
    return render_template("admin/dashboard.html", stats=panel.estadisticas())


# Esto sirve para: leer y validar los filtros de la URL (búsqueda, país, estado, área)
def _leer_filtros():
    estado = request.args.get("estado", "")
    pais = request.args.get("pais", "")
    return {
        "q": request.args.get("q", "").strip()[:100],
        "pais": pais if pais in PAISES else "",
        "estado": estado if estado in ESTADOS else "",
        "area": request.args.get("area", type=int),
    }


# Esto sirve para: listar solicitudes con filtros y paginación
@admin_bp.route("/colaboradores")
@admin_requerido
def listado():
    filtros = _leer_filtros()
    pagina = max(request.args.get("pagina", 1, type=int), 1)
    filas, total = panel.listar(filtros, pagina, POR_PAGINA)
    total_paginas = max(1, math.ceil(total / POR_PAGINA))
    if pagina > total_paginas:
        pagina = total_paginas
        filas, total = panel.listar(filtros, pagina, POR_PAGINA)

    return render_template(
        "admin/listado.html", filas=filas, total=total, pagina=pagina,
        total_paginas=total_paginas, filtros=filtros,
        parametros={k: v for k, v in filtros.items() if v},
        paises=PAISES, estados=ESTADOS, areas=colaboradores.obtener_areas())


# Esto sirve para: ver el detalle de una solicitud
@admin_bp.route("/colaboradores/<int:colaborador_id>")
@admin_requerido
def detalle(colaborador_id):
    colaborador = panel.detalle(colaborador_id)
    if colaborador is None:
        abort(404)
    return render_template("admin/detalle.html", c=colaborador, estados=ESTADOS)


# ---------- U: Actualizar ----------
# Esto sirve para: editar una solicitud (muestra el formulario y guarda los cambios validados)
@admin_bp.route("/colaboradores/<int:colaborador_id>/editar", methods=["GET", "POST"])
@admin_requerido
def editar(colaborador_id):
    datos = panel.detalle(colaborador_id)
    if datos is None:
        abort(404)
    areas_disponibles = colaboradores.obtener_areas()

    if request.method == "POST":
        colaborador = Colaborador.desde_formulario(request.form)
        errores = colaborador.validar()

        seleccion = request.form.getlist("areas")
        validas = {str(a["id"]) for a in areas_disponibles}
        if not seleccion or any(a not in validas for a in seleccion):
            errores.append("Selecciona al menos un área de colaboración válida.")

        if not errores:
            try:
                if not colaboradores.actualizar(colaborador_id, colaborador, seleccion):
                    abort(404)
                flash("Los datos se actualizaron correctamente.", "ok")
                return redirect(url_for("admin.detalle", colaborador_id=colaborador_id))
            except CorreoDuplicadoError:
                errores.append("Ese correo ya pertenece a otra solicitud.")

        for error in errores:
            flash(error, "error")
        # Se vuelve a mostrar lo que la persona escribió, no lo guardado
        datos = {
            "id": colaborador_id, "nombre_completo": colaborador.nombre,
            "pais": colaborador.pais, "correo": colaborador.correo,
            "telefono": colaborador.telefono, "modalidad": colaborador.modalidad,
            "disponibilidad": colaborador.disponibilidad,
            "motivacion": colaborador.motivacion,
            "area_ids": [int(a) for a in seleccion if a.isdigit()],
        }

    return render_template("admin/editar.html", c=datos, areas=areas_disponibles,
                           paises=PAISES, modalidades=MODALIDADES,
                           disponibilidades=DISPONIBILIDADES)


# Esto sirve para: cambiar el estado (Pendiente, Aprobado, etc.)
@admin_bp.route("/colaboradores/<int:colaborador_id>/estado", methods=["POST"])
@admin_requerido
def cambiar_estado(colaborador_id):
    estado = request.form.get("estado", "")
    if estado not in ESTADOS:
        flash("Estado no válido.", "error")
    elif panel.cambiar_estado(colaborador_id, estado) == 0:
        abort(404)
    else:
        flash(f"La solicitud quedó como «{estado}».", "ok")
    return redirect(url_for("admin.detalle", colaborador_id=colaborador_id))


# ---------- D: Eliminar ----------
# Esto sirve para: eliminar una solicitud
@admin_bp.route("/colaboradores/<int:colaborador_id>/eliminar", methods=["POST"])
@admin_requerido
def eliminar(colaborador_id):
    if not colaboradores.eliminar(colaborador_id):
        abort(404)
    flash("La solicitud fue eliminada.", "ok")
    return redirect(url_for("admin.listado"))


# ---------- Exportación ----------
# Esto sirve para: descargar las solicitudes (con los filtros activos) en Excel
@admin_bp.route("/exportar")
@admin_requerido
def exportar():
    filas, _ = panel.listar(_leer_filtros())     # respeta los filtros activos
    nombre = f"colaboradores_{datetime.now():%Y-%m-%d}.xlsx"
    return send_file(
        crear_excel(filas), as_attachment=True, download_name=nombre,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
