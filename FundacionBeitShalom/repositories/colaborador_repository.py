from repositories.base_repository import BaseRepository


# Esto sirve para: señalar que el correo ya está registrado
class CorreoDuplicadoError(Exception):
    """El correo ya existe en la base de datos."""


# Esto sirve para: detectar si el error de SQL fue por correo repetido
def _es_correo_duplicado(error):
    return "UQ_Colaboradores_Correo" in str(error)


# Esto sirve para: hacer el CRUD de colaboradores (todo el SQL está aquí)
class ColaboradorRepository(BaseRepository):
    """CRUD de colaboradores. Aquí vive el SQL; ningún otro archivo lo tiene."""

    # Esto sirve para: leer las áreas de colaboración activas
    def obtener_areas(self):
        """Lee las áreas activas: [{'id': 1, 'nombre': '...'}, ...]"""
        with self._conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM AreasColaboracion "
                           "WHERE activa = 1 ORDER BY id")
            return [{"id": fila.id, "nombre": fila.nombre}
                    for fila in cursor.fetchall()]

    # Esto sirve para: vincular un colaborador con sus áreas
    def _guardar_areas(self, cursor, colaborador_id, areas):
        for area_id in areas:
            cursor.execute(
                "INSERT INTO ColaboradorAreas (colaborador_id, area_id) VALUES (?, ?)",
                (colaborador_id, int(area_id)))

    # ---------- C: Crear ----------
    # Esto sirve para: crear un colaborador y sus áreas en una sola transacción
    def guardar(self, colaborador, areas):
        """Guarda al colaborador y sus áreas en una sola transacción."""
        try:
            with self._transaccion() as cursor:
                cursor.execute("""
                    INSERT INTO Colaboradores (
                        nombre_completo, pais, correo, telefono, modalidad,
                        disponibilidad, motivacion, acepta_privacidad
                    )
                    OUTPUT INSERTED.id
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    colaborador.nombre, colaborador.pais, colaborador.correo,
                    colaborador.telefono or None, colaborador.modalidad,
                    colaborador.disponibilidad, colaborador.motivacion or None, 1,
                ))
                colaborador_id = cursor.fetchone()[0]
                self._guardar_areas(cursor, colaborador_id, areas)
                return colaborador_id
        except Exception as error:
            if _es_correo_duplicado(error):
                raise CorreoDuplicadoError() from error
            raise

    # ---------- U: Actualizar ----------
    # Esto sirve para: modificar los datos y las áreas de un colaborador
    def actualizar(self, colaborador_id, colaborador, areas):
        """Cambia los datos y las áreas. Devuelve False si el id no existe."""
        try:
            with self._transaccion() as cursor:
                cursor.execute("""
                    UPDATE Colaboradores
                    SET nombre_completo = ?, pais = ?, correo = ?, telefono = ?,
                        modalidad = ?, disponibilidad = ?, motivacion = ?
                    WHERE id = ?
                """, (
                    colaborador.nombre, colaborador.pais, colaborador.correo,
                    colaborador.telefono or None, colaborador.modalidad,
                    colaborador.disponibilidad, colaborador.motivacion or None,
                    colaborador_id,
                ))
                if cursor.rowcount == 0:
                    return False
                cursor.execute("DELETE FROM ColaboradorAreas WHERE colaborador_id = ?",
                               (colaborador_id,))
                self._guardar_areas(cursor, colaborador_id, areas)
                return True
        except Exception as error:
            if _es_correo_duplicado(error):
                raise CorreoDuplicadoError() from error
            raise

    # ---------- D: Eliminar ----------
    # Esto sirve para: borrar un colaborador y sus áreas
    def eliminar(self, colaborador_id):
        """Borra al colaborador y sus áreas. Devuelve False si el id no existe."""
        with self._transaccion() as cursor:
            # Primero la tabla hija (ColaboradorAreas), luego la principal
            cursor.execute("DELETE FROM ColaboradorAreas WHERE colaborador_id = ?",
                           (colaborador_id,))
            cursor.execute("DELETE FROM Colaboradores WHERE id = ?", (colaborador_id,))
            return cursor.rowcount > 0
