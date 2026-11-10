"""Objetos falsos para probar sin necesitar SQL Server."""
from datetime import datetime

from werkzeug.security import generate_password_hash

from models.administrador import Administrador
from repositories.colaborador_repository import CorreoDuplicadoError

FILA = {
    "id": 1, "nombre_completo": "=Ana Prueba", "pais": "El Salvador",
    "correo": "ana@ejemplo.com", "telefono": "+503 2222-1234",
    "modalidad": "Virtual", "disponibilidad": "Ocasional", "estado": "Pendiente",
    "fecha_registro": datetime(2026, 11, 6, 10, 30),
    "areas": ["Apoyo educativo"], "area_ids": [3],
}
AREAS = [{"id": 1, "nombre": "Voluntariado presencial"}, {"id": 3, "nombre": "Apoyo educativo"}]


class AdministradoresFalsos:
    def obtener_por_usuario(self, usuario):
        if usuario == "admin":
            return Administrador(1, "admin", "Admin Prueba",
                                 generate_password_hash("clave1234"), True)
        return None


class PanelFalso:
    def estadisticas(self):
        return {"total": 1,
                "por_estado": {"Pendiente": 1, "En revisión": 0, "Aprobado": 0, "Rechazado": 0},
                "por_pais": [{"pais": "El Salvador", "total": 1}],
                "por_area": [{"nombre": "Apoyo educativo", "total": 1}],
                "recientes": [FILA]}

    def listar(self, filtros, pagina=None, por_pagina=None):
        return [FILA], 1

    def detalle(self, colaborador_id):
        if colaborador_id != 1:
            return None
        return dict(FILA, motivacion="Quiero ayudar", acepta_privacidad=True)

    def cambiar_estado(self, colaborador_id, estado):
        return 1


class ColaboradoresFalsos:
    """Hace de ColaboradorRepository y anota lo que se le pide."""

    def __init__(self):
        self.guardados, self.actualizados, self.eliminados = [], [], []
        self.error = None

    def obtener_areas(self):
        return AREAS

    def guardar(self, colaborador, areas):
        if self.error:
            raise self.error
        self.guardados.append((colaborador, areas))
        return 1

    def actualizar(self, colaborador_id, colaborador, areas):
        if self.error:
            raise self.error
        self.actualizados.append((colaborador_id, colaborador, areas))
        return True

    def eliminar(self, colaborador_id):
        self.eliminados.append(colaborador_id)
        return True


def correo_duplicado():
    return CorreoDuplicadoError()
