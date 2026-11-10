from flask import Blueprint, render_template

# Esto sirve para: agrupar las páginas informativas del sitio
sitio_bp = Blueprint("sitio", __name__)


# Esto sirve para: mostrar la página de inicio
@sitio_bp.route("/")
def inicio():
    return render_template("sitio/inicio.html")


# Esto sirve para: mostrar la página Nosotros
@sitio_bp.route("/nosotros")
def nosotros():
    return render_template("sitio/nosotros.html")


# Esto sirve para: mostrar la página de Programas
@sitio_bp.route("/programas")
def programas():
    return render_template("sitio/programas.html")


# Esto sirve para: mostrar la página de Proyectos
@sitio_bp.route("/proyectos")
def proyectos():
    return render_template("sitio/proyectos.html")


# Esto sirve para: mostrar la página de Eventos
@sitio_bp.route("/eventos")
def eventos():
    return render_template("sitio/eventos.html")


# Esto sirve para: mostrar la galería de fotos
@sitio_bp.route("/galeria")
def galeria():
    return render_template("sitio/galeria.html")


# Esto sirve para: mostrar las noticias
@sitio_bp.route("/noticias")
def noticias():
    return render_template("sitio/noticias.html")


# Esto sirve para: mostrar la página de contacto
@sitio_bp.route("/contacto")
def contacto():
    return render_template("sitio/contacto.html")
