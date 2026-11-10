from werkzeug.security import check_password_hash

from models.persona import Persona


# Esto sirve para: representar a un administrador del panel
class Administrador(Persona):
    """Persona del personal autorizado para entrar al panel. Hereda de Persona."""

    def __init__(self, id, usuario, nombre, password_hash, activo=True):
        super().__init__(nombre)
        self.id = id
        self.usuario = usuario
        self.activo = activo
        self._password_hash = password_hash   # privado: no se usa fuera de la clase

    # Esto sirve para: comprobar la contraseña contra el hash guardado
    def verificar_password(self, password):
        """True solo si la cuenta está activa y la contraseña coincide con el hash."""
        return self.activo and check_password_hash(self._password_hash, password)
