import io
import unittest
from unittest import mock

import openpyxl

import controllers.admin_controller as ac
from app import app
from tests.falsos import (AdministradoresFalsos, ColaboradoresFalsos,
                          PanelFalso, correo_duplicado)

DATOS = {
    "nombre": "Ana María López", "pais": "El Salvador", "correo": "ana@ejemplo.com",
    "telefono": "7777-0001", "modalidad": "Virtual", "disponibilidad": "Ocasional",
    "motivacion": "Quiero ayudar", "areas": ["1"],
}


class PruebasPanel(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.colaboradores = ColaboradoresFalsos()
        for nombre, falso in (("admins", AdministradoresFalsos()), ("panel", PanelFalso()),
                              ("colaboradores", self.colaboradores)):
            parche = mock.patch.object(ac, nombre, falso)
            parche.start()
            self.addCleanup(parche.stop)
        self.cliente = app.test_client()

    def entrar(self):
        respuesta = self.cliente.post(
            "/admin/login", data={"usuario": "admin", "password": "clave1234"})
        self.assertEqual(respuesta.status_code, 302)

    def texto(self, respuesta):
        return respuesta.get_data(as_text=True)

    # ----- acceso -----
    def test_rutas_protegidas_piden_login(self):
        for url in ("/admin/", "/admin/colaboradores", "/admin/colaboradores/1",
                    "/admin/colaboradores/1/editar", "/admin/exportar"):
            respuesta = self.cliente.get(url)
            self.assertEqual(respuesta.status_code, 302, url)
            self.assertIn("/admin/login", respuesta.headers["Location"])

    def test_no_se_puede_eliminar_sin_sesion(self):
        self.cliente.post("/admin/colaboradores/1/eliminar")
        self.assertEqual(self.colaboradores.eliminados, [])

    def test_login_con_contrasena_mala(self):
        for usuario, clave in (("admin", "mala"), ("nadie", "x")):
            respuesta = self.cliente.post("/admin/login",
                                          data={"usuario": usuario, "password": clave})
            self.assertIn("incorrectos", self.texto(respuesta))

    def test_logout_cierra_la_sesion(self):
        self.entrar()
        self.cliente.post("/admin/logout")
        self.assertEqual(self.cliente.get("/admin/").status_code, 302)

    # ----- leer -----
    def test_las_pantallas_cargan(self):
        self.entrar()
        for url in ("/admin/", "/admin/colaboradores",
                    "/admin/colaboradores?q=ana&estado=Pendiente&area=1&pais=El+Salvador",
                    "/admin/colaboradores/1", "/admin/colaboradores/1/editar"):
            self.assertEqual(self.cliente.get(url).status_code, 200, url)

    def test_detalle_inexistente_da_404(self):
        self.entrar()
        self.assertEqual(self.cliente.get("/admin/colaboradores/99").status_code, 404)

    def test_pagina_404_amigable(self):
        respuesta = self.cliente.get("/no-existe")
        self.assertEqual(respuesta.status_code, 404)
        self.assertIn("no existe", self.texto(respuesta))

    # ----- actualizar -----
    def test_editar_guarda_los_cambios(self):
        self.entrar()
        respuesta = self.cliente.post("/admin/colaboradores/1/editar", data=DATOS)
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(len(self.colaboradores.actualizados), 1)

    def test_editar_con_datos_malos_no_guarda(self):
        self.entrar()
        respuesta = self.cliente.post("/admin/colaboradores/1/editar",
                                      data=dict(DATOS, correo="malo"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("El correo no es válido.", self.texto(respuesta))
        self.assertEqual(self.colaboradores.actualizados, [])

    def test_editar_con_correo_repetido(self):
        self.entrar()
        self.colaboradores.error = correo_duplicado()
        respuesta = self.cliente.post("/admin/colaboradores/1/editar", data=DATOS)
        self.assertIn("pertenece a otra solicitud", self.texto(respuesta))

    def test_cambiar_estado(self):
        self.entrar()
        self.cliente.post("/admin/colaboradores/1/estado", data={"estado": "Aprobado"})
        self.assertIn("quedó como", self.texto(self.cliente.get("/admin/colaboradores/1")))

    def test_estado_invalido_se_rechaza(self):
        self.entrar()
        self.cliente.post("/admin/colaboradores/1/estado", data={"estado": "Hackeado"})
        self.assertIn("Estado no válido", self.texto(self.cliente.get("/admin/colaboradores/1")))

    # ----- eliminar -----
    def test_eliminar(self):
        self.entrar()
        respuesta = self.cliente.post("/admin/colaboradores/1/eliminar")
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(self.colaboradores.eliminados, [1])

    # ----- exportar -----
    def test_exportar_excel_y_neutralizar_formulas(self):
        self.entrar()
        respuesta = self.cliente.get("/admin/exportar")
        self.assertEqual(respuesta.data[:2], b"PK")
        hoja = openpyxl.load_workbook(io.BytesIO(respuesta.data)).active
        self.assertEqual(hoja["B2"].value, "'=Ana Prueba")
