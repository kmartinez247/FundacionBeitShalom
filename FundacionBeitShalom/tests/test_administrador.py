import unittest

from werkzeug.security import generate_password_hash

from models.administrador import Administrador
from models.persona import Persona


def crear(activo=True):
    return Administrador(1, "admin", " Admin Prueba ", generate_password_hash("clave1234"), activo)


class PruebasAdministrador(unittest.TestCase):
    def test_contrasena_correcta(self):
        self.assertTrue(crear().verificar_password("clave1234"))

    def test_contrasena_incorrecta(self):
        self.assertFalse(crear().verificar_password("otra"))

    def test_cuenta_inactiva_no_entra(self):
        self.assertFalse(crear(activo=False).verificar_password("clave1234"))

    def test_hereda_de_persona(self):
        admin = crear()
        self.assertIsInstance(admin, Persona)
        self.assertEqual(str(admin), "Admin Prueba")
