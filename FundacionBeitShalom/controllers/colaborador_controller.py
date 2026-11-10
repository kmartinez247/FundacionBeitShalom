from flask import (Blueprint, current_app, flash, redirect,
                   render_template, request, url_for)

from models.colaborador import (Colaborador, PAISES,
                                MODALIDADES, DISPONIBILIDADES)
from repositories.colaborador_repository import (ColaboradorRepository,
                                                 CorreoDuplicadoError)

# Esto sirve para: agrupar las rutas públicas de registro
colaborador_bp = Blueprint("colaborador", __name__)
# Esto sirve para: acceder a la base de datos de colaboradores
repositorio = ColaboradorRepository()


# Esto sirve para: traer las áreas de colaboración sin romper la página si falla la base de datos
def _cargar_areas():
    try:
        return repositorio.obtener_areas()
    except Exception:
        current_app.logger.exception("No se pudieron leer las áreas")
        flash("No se pudo conectar con la base de datos. Intenta más tarde.", "error")
        return []


# Esto sirve para: mostrar el formulario de registro y guardar la solicitud si es válida
@colaborador_bp.route("/registro", methods=["GET", "POST"])
def registrar():
    """Formulario público: GET lo muestra, POST valida y guarda la solicitud."""
    areas_disponibles = _cargar_areas()

    if request.method == "POST":
        colaborador = Colaborador.desde_formulario(request.form)
        errores = colaborador.validar()

        seleccion = request.form.getlist("areas")
        validas = {str(a["id"]) for a in areas_disponibles}
        if not seleccion or any(a not in validas for a in seleccion):
            errores.append("Selecciona al menos un área de colaboración válida.")

        if request.form.get("privacidad") != "1":
            errores.append("Debes aceptar la política de privacidad.")

        if not errores:
            try:
                repositorio.guardar(colaborador, seleccion)
                return redirect(url_for("colaborador.confirmacion"))
            except CorreoDuplicadoError:
                errores.append("Este correo ya tiene una solicitud registrada.")
            except Exception:
                current_app.logger.exception("Error al guardar la solicitud")
                errores.append("No pudimos guardar tu solicitud. Intenta de nuevo.")

        for error in errores:
            flash(error, "error")

    return render_template("registro.html", areas=areas_disponibles,
                           paises=PAISES, modalidades=MODALIDADES,
                           disponibilidades=DISPONIBILIDADES)


# Esto sirve para: mostrar la página de 'solicitud enviada'
@colaborador_bp.route("/confirmacion")
def confirmacion():
    return render_template("confirmacion.html")


# Esto sirve para: mostrar la política de privacidad
@colaborador_bp.route("/privacidad")
def privacidad():
    return render_template("privacidad.html")
