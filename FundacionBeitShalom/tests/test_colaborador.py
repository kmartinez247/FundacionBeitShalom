import unittest

from models.colaborador import Colaborador


def crear(**cambios):
    datos = dict(nombre="Ana María López", pais="El Salvador", correo="ana@ejemplo.com",
                 telefono="7777-0001", modalidad="Virtual", disponibilidad="Ocasional",
                 motivacion="Quiero ayudar")
    datos.update(cambios)
    return Colaborador(**datos)


class PruebasColaborador(unittest.TestCase):
    def test_datos_correctos_no_dan_errores(self):
        self.assertEqual(crear().validar(), [])

    def test_nombre_muy_corto(self):
        self.assertEqual(len(crear(nombre="Ana").validar()), 1)

    def test_correo_invalido(self):
        self.assertIn("El correo no es válido.", crear(correo="hola").validar())

    def test_pais_invalido(self):
        self.assertIn("Debes seleccionar un país.", crear(pais="").validar())

    def test_telefono_es_opcional(self):
        self.assertEqual(crear(telefono="").validar(), [])

    def test_telefono_invalido(self):
        self.assertIn("El teléfono no es válido.", crear(telefono="abc").validar())

    def test_modalidad_y_disponibilidad_invalidas(self):
        self.assertEqual(len(crear(modalidad="X", disponibilidad="Y").validar()), 2)

    def test_motivacion_muy_larga(self):
        self.assertEqual(len(crear(motivacion="a" * 1001).validar()), 1)

    def test_encapsulamiento_limpia_espacios(self):
        colaborador = crear(nombre="  Ana María López  ", correo=" ana@ejemplo.com ")
        self.assertEqual(colaborador.nombre, "Ana María López")
        colaborador.correo = "  otro@ejemplo.com "
        self.assertEqual(colaborador.correo, "otro@ejemplo.com")

    def test_none_se_vuelve_texto_vacio(self):
        self.assertEqual(crear(telefono=None).telefono, "")

    def test_desde_formulario(self):
        colaborador = Colaborador.desde_formulario({"nombre": "Ana María López"})
        self.assertEqual(colaborador.nombre, "Ana María López")
        self.assertEqual(colaborador.pais, "")

    def test_polimorfismo_str(self):
        self.assertEqual(str(crear()), "Ana María López <ana@ejemplo.com>")
