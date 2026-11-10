# Esto sirve para: ser la clase base (nombre) de Colaborador y Administrador
class Persona:
    """Clase padre: lo que comparten colaboradores y administradores (el nombre)."""

    def __init__(self, nombre):
        self.nombre = nombre   # pasa por el setter, que limpia los espacios

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = (valor or "").strip()

    def __str__(self):
        return self.nombre
