from contextlib import contextmanager

from database import obtener_conexion


# Esto sirve para: ser la clase base que maneja las conexiones a la base de datos
class BaseRepository:
    """Clase padre de los repositories: abre, confirma y cierra las conexiones."""

    # Esto sirve para: abrir y cerrar la conexión automáticamente en lecturas
    @contextmanager
    def _conexion(self):
        """Para consultas de lectura: abre la conexión y siempre la cierra."""
        conexion = obtener_conexion()
        try:
            yield conexion
        finally:
            conexion.close()

    # Esto sirve para: guardar cambios (commit) o deshacerlos (rollback) en escrituras
    @contextmanager
    def _transaccion(self):
        """Para escrituras: si todo sale bien hace commit; si algo falla, rollback."""
        with self._conexion() as conexion:
            try:
                yield conexion.cursor()
                conexion.commit()
            except Exception:
                conexion.rollback()
                raise
