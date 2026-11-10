import unittest
from unittest import mock

import controllers.colaborador_controller as cc
from app import app
from tests.falsos import ColaboradoresFalsos, correo_duplicado

DATOS = {
    "nombre": "Ana María López", "pais": "El Salvador", "correo": "ana@ejemplo.com",
    "telefono": "7777-0001", "modalidad": "Virtual", "disponibilidad": "Ocasional",
    "motivacion": "Quiero ayudar", "areas": ["1", "3"], "privacidad": "1",
}


class PruebasRegistro(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
        self.repo = ColaboradoresFalsos()
        parche = mock.patch.object(cc, "repositorio", self.repo)
        parche.start()
        self.addCleanup(parche.stop)
        self.cliente = app.test_client()

    def enviar(self, **cambios):
        datos = dict(DATOS)
        datos.update(cambios)
        return self.cliente.post("/registro", data=datos)

    def test_el_formulario_carga(self):
        respuesta = self.cliente.get("/registro")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("¡Queremos conocerte!", respuesta.get_data(as_text=True))

    def test_pagina_de_privacidad(self):
        self.assertEqual(self.cliente.get("/privacidad").status_code, 200)

    def test_envio_correcto_guarda_y_confirma(self):
        respuesta = self.enviar()
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/confirmacion", respuesta.headers["Location"])
        self.assertEqual(len(self.repo.guardados), 1)

    def test_formulario_vacio_no_guarda(self):
        respuesta = self.cliente.post("/registro", data={})
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("El nombre completo debe tener", respuesta.get_data(as_text=True))
        self.assertEqual(self.repo.guardados, [])

    def test_correo_incorrecto(self):
        respuesta = self.enviar(correo="hola")
        self.assertIn("El correo no es válido.", respuesta.get_data(as_text=True))
        self.assertEqual(self.repo.guardados, [])

    def test_sin_areas(self):
        respuesta = self.enviar(areas=[])
        self.assertIn("Selecciona al menos un área", respuesta.get_data(as_text=True))
        self.assertEqual(self.repo.guardados, [])

    def test_area_que_no_existe(self):
        self.enviar(areas=["99"])
        self.assertEqual(self.repo.guardados, [])

    def test_sin_aceptar_privacidad(self):
        respuesta = self.enviar(privacidad="")
        self.assertIn("Debes aceptar la política", respuesta.get_data(as_text=True))
        self.assertEqual(self.repo.guardados, [])

    def test_correo_duplicado(self):
        self.repo.error = correo_duplicado()
        respuesta = self.enviar()
        self.assertIn("ya tiene una solicitud", respuesta.get_data(as_text=True))
