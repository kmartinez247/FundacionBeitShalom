import unittest
from unittest import mock

from models.colaborador import Colaborador
from repositories.base_repository import BaseRepository
from repositories.colaborador_repository import ColaboradorRepository, CorreoDuplicadoError


class CursorFalso:
    def __init__(self, error=None, filas_afectadas=1):
        self.error, self.rowcount, self.sentencias = error, filas_afectadas, []

    def execute(self, sql, *params):
        self.sentencias.append(sql)
        if self.error and "INSERT INTO Colaboradores" in sql:
            raise self.error

    def fetchone(self):
        return (7,)


class ConexionFalsa:
    def __init__(self, cursor):
        self._cursor = cursor
        self.confirmadas = self.revertidas = 0
        self.cerrada = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.confirmadas += 1

    def rollback(self):
        self.revertidas += 1

    def close(self):
        self.cerrada = True


def con_conexion(conexion):
    return mock.patch("repositories.base_repository.obtener_conexion", return_value=conexion)


def colaborador():
    return Colaborador("Ana María López", "El Salvador", "ana@ejemplo.com", "7777-0001",
                       "Virtual", "Ocasional", "Hola")


class PruebasTransacciones(unittest.TestCase):
    def test_si_todo_sale_bien_hace_commit(self):
        conexion = ConexionFalsa(CursorFalso())
        with con_conexion(conexion):
            with BaseRepository()._transaccion():
                pass
        self.assertEqual((conexion.confirmadas, conexion.revertidas), (1, 0))
        self.assertTrue(conexion.cerrada)

    def test_si_algo_falla_hace_rollback(self):
        conexion = ConexionFalsa(CursorFalso())
        with con_conexion(conexion):
            with self.assertRaises(ValueError):
                with BaseRepository()._transaccion():
                    raise ValueError("fallo simulado")
        self.assertEqual((conexion.confirmadas, conexion.revertidas), (0, 1))
        self.assertTrue(conexion.cerrada)


class PruebasColaboradorRepository(unittest.TestCase):
    def test_guardar_inserta_colaborador_y_sus_areas(self):
        cursor = CursorFalso()
        conexion = ConexionFalsa(cursor)
        with con_conexion(conexion):
            nuevo_id = ColaboradorRepository().guardar(colaborador(), ["1", "2"])
        self.assertEqual(nuevo_id, 7)
        areas = [s for s in cursor.sentencias if "INSERT INTO ColaboradorAreas" in s]
        self.assertEqual(len(areas), 2)
        self.assertEqual(conexion.confirmadas, 1)

    def test_correo_duplicado_revierte_y_avisa(self):
        error = Exception("Violation of UNIQUE KEY constraint 'UQ_Colaboradores_Correo'")
        conexion = ConexionFalsa(CursorFalso(error=error))
        with con_conexion(conexion):
            with self.assertRaises(CorreoDuplicadoError):
                ColaboradorRepository().guardar(colaborador(), ["1"])
        self.assertEqual((conexion.confirmadas, conexion.revertidas), (0, 1))

    def test_eliminar_borra_primero_las_areas(self):
        cursor = CursorFalso()
        with con_conexion(ConexionFalsa(cursor)):
            self.assertTrue(ColaboradorRepository().eliminar(1))
        self.assertIn("ColaboradorAreas", cursor.sentencias[0])
        self.assertIn("DELETE FROM Colaboradores", cursor.sentencias[1])

    def test_eliminar_id_inexistente(self):
        with con_conexion(ConexionFalsa(CursorFalso(filas_afectadas=0))):
            self.assertFalse(ColaboradorRepository().eliminar(99))

    def test_actualizar_id_inexistente(self):
        with con_conexion(ConexionFalsa(CursorFalso(filas_afectadas=0))):
            self.assertFalse(ColaboradorRepository().actualizar(99, colaborador(), ["1"]))
