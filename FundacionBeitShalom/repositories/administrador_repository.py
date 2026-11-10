from models.administrador import Administrador
from repositories.base_repository import BaseRepository


# Esto sirve para: consultar y crear administradores en la base de datos
class AdministradorRepository(BaseRepository):
    # Esto sirve para: buscar un administrador por su usuario (para el login)
    def obtener_por_usuario(self, usuario):
        """Devuelve el Administrador o None si el usuario no existe."""
        with self._conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, usuario, nombre, password_hash, activo "
                           "FROM Administradores WHERE usuario = ?", (usuario,))
            fila = cursor.fetchone()
            if not fila:
                return None
            return Administrador(fila.id, fila.usuario, fila.nombre,
                                 fila.password_hash, bool(fila.activo))

    # Esto sirve para: insertar un nuevo administrador
    def crear(self, usuario, nombre, password_hash):
        with self._transaccion() as cursor:
            cursor.execute("INSERT INTO Administradores (usuario, nombre, password_hash) "
                           "VALUES (?, ?, ?)", (usuario, nombre, password_hash))
