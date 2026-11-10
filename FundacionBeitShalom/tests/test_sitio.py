import unittest

from app import app

RUTAS = ["/", "/nosotros", "/programas", "/proyectos",
         "/eventos", "/galeria", "/noticias", "/contacto"]


class PruebasSitio(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.cliente = app.test_client()

    def test_las_paginas_del_sitio_cargan(self):
        for ruta in RUTAS:
            respuesta = self.cliente.get(ruta)
            self.assertEqual(respuesta.status_code, 200, ruta)
            self.assertIn("Fundación Beit Shalom", respuesta.get_data(as_text=True), ruta)

    def test_el_menu_lleva_al_formulario(self):
        texto = self.cliente.get("/").get_data(as_text=True)
        self.assertIn('href="/registro"', texto)
        self.assertIn("Colaborar", texto)

    def test_el_inicio_invita_a_colaborar(self):
        self.assertIn("Quiero colaborar", self.cliente.get("/").get_data(as_text=True))

    def test_no_quedan_enlaces_viejos(self):
        for ruta in RUTAS:
            texto = self.cliente.get(ruta).get_data(as_text=True)
            self.assertNotIn('.html"', texto, ruta)
            self.assertNotIn('"assets/', texto, ruta)

    def test_los_archivos_de_la_plantilla_existen(self):
        for ruta in ("/static/css/kidearn.css", "/static/css/beit-shalom.css",
                     "/static/css/colaboradores.css", "/static/js/kidearn.js",
                     "/static/vendors/bootstrap/css/bootstrap.min.css"):
            respuesta = self.cliente.get(ruta)
            respuesta.close()
            self.assertEqual(respuesta.status_code, 200, ruta)

    def test_el_formulario_usa_el_diseno_del_sitio(self):
        texto = self.cliente.get("/registro").get_data(as_text=True)
        self.assertIn("page-header", texto)
        self.assertIn("main-footer", texto)
