from datetime import timedelta

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect, CSRFError

from config import Config
from controllers.admin_controller import admin_bp
from controllers.colaborador_controller import colaborador_bp
from controllers.sitio_controller import sitio_bp

# Esto sirve para: crear la aplicación Flask y cargar la configuración
app = Flask(__name__)
app.config.from_object(Config)
# Esto sirve para: proteger la cookie de sesión y limitar su duración a 2 horas
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2),
)

# Esto sirve para: activar la protección CSRF en todos los formularios
CSRFProtect(app)
# Esto sirve para: conectar las rutas del sitio público, el registro y el panel admin
app.register_blueprint(sitio_bp)
app.register_blueprint(colaborador_bp)
app.register_blueprint(admin_bp)


# Esto sirve para: avisar y redirigir cuando el formulario expiró (token CSRF inválido)
@app.errorhandler(CSRFError)
def error_csrf(error):
    flash("El formulario expiró. Intenta de nuevo.", "error")
    destino = "admin.login" if request.path.startswith("/admin") else "colaborador.registrar"
    return redirect(url_for(destino))


# Esto sirve para: mostrar la plantilla de error con su código HTTP
def _pagina_error(codigo, titulo, mensaje):
    return render_template("error.html", codigo=codigo, titulo=titulo,
                           mensaje=mensaje), codigo


# Esto sirve para: mostrar la página de 'no encontrada'
@app.errorhandler(404)
def no_encontrado(error):
    return _pagina_error(404, "Página no encontrada", "La página que buscas no existe.")


# Esto sirve para: mostrar la página de 'acción no permitida'
@app.errorhandler(405)
def metodo_no_permitido(error):
    return _pagina_error(405, "Acción no permitida", "Esa acción no está disponible aquí.")


# Esto sirve para: mostrar la página de error interno
@app.errorhandler(500)
def error_interno(error):
    return _pagina_error(500, "Algo salió mal",
                         "Ocurrió un error inesperado. Intenta de nuevo en unos minutos.")


# Esto sirve para: arrancar el servidor al ejecutar `python app.py`
if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
