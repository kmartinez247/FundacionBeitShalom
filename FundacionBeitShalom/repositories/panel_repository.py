from models.colaborador import ESTADOS
from repositories.base_repository import BaseRepository


# Esto sirve para: convertir las filas de SQL en diccionarios
def _a_dicts(cursor):
    columnas = [c[0] for c in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]


# Esto sirve para: añadir a cada colaborador la lista de sus áreas
def _agregar_areas(cursor, filas):
    """Agrega a cada colaborador sus áreas: nombres (areas) e identificadores (area_ids)."""
    por_id = {f["id"]: f for f in filas}
    for f in filas:
        f["areas"] = []
        f["area_ids"] = []
    ids = list(por_id)
    for i in range(0, len(ids), 1000):          # SQL Server limita los parámetros
        grupo = ids[i:i + 1000]
        marcas = ",".join("?" * len(grupo))     # solo signos "?", los valores van aparte
        cursor.execute(
            "SELECT ca.colaborador_id, a.id, a.nombre FROM ColaboradorAreas ca "
            "JOIN AreasColaboracion a ON a.id = ca.area_id "
            f"WHERE ca.colaborador_id IN ({marcas}) ORDER BY a.id", *grupo)
        for colaborador_id, area_id, nombre in cursor.fetchall():
            por_id[colaborador_id]["area_ids"].append(area_id)
            por_id[colaborador_id]["areas"].append(nombre)


# Esto sirve para: hacer las consultas del panel admin
class PanelRepository(BaseRepository):
    """Lecturas del panel (R de CRUD) y cambio de estado. Todo con parámetros."""

    # Esto sirve para: armar el WHERE del SQL según los filtros, con parámetros seguros
    def _donde(self, filtros):
        condiciones, params = [], []
        if filtros.get("q"):
            patron = f"%{filtros['q']}%"
            condiciones.append("(c.nombre_completo LIKE ? OR c.correo LIKE ?)")
            params += [patron, patron]
        if filtros.get("pais"):
            condiciones.append("c.pais = ?")
            params.append(filtros["pais"])
        if filtros.get("estado"):
            condiciones.append("c.estado = ?")
            params.append(filtros["estado"])
        if filtros.get("area"):
            condiciones.append("EXISTS (SELECT 1 FROM ColaboradorAreas x "
                               "WHERE x.colaborador_id = c.id AND x.area_id = ?)")
            params.append(filtros["area"])
        donde = (" WHERE " + " AND ".join(condiciones)) if condiciones else ""
        return donde, params

    # Esto sirve para: obtener solicitudes filtradas y paginadas, más el total
    def listar(self, filtros, pagina=None, por_pagina=None):
        """Devuelve (filas, total). Sin pagina/por_pagina devuelve todas las filas."""
        donde, params = self._donde(filtros)
        with self._conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM Colaboradores c{donde}", *params)
            total = cursor.fetchone()[0]

            sql = ("SELECT c.id, c.nombre_completo, c.pais, c.correo, c.telefono, "
                   "c.modalidad, c.disponibilidad, c.estado, c.fecha_registro "
                   f"FROM Colaboradores c{donde} "
                   "ORDER BY c.fecha_registro DESC, c.id DESC")
            datos = list(params)
            if pagina and por_pagina:
                sql += " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
                datos += [(pagina - 1) * por_pagina, por_pagina]
            cursor.execute(sql, *datos)
            filas = _a_dicts(cursor)
            _agregar_areas(cursor, filas)
            return filas, total

    # Esto sirve para: obtener todos los datos de una solicitud
    def detalle(self, colaborador_id):
        """Devuelve un dict con todos los datos de la persona, o None."""
        with self._conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre_completo, pais, correo, telefono, modalidad, "
                "disponibilidad, motivacion, acepta_privacidad, fecha_registro, estado "
                "FROM Colaboradores WHERE id = ?", colaborador_id)
            filas = _a_dicts(cursor)
            if not filas:
                return None
            _agregar_areas(cursor, filas)
            return filas[0]

    # Esto sirve para: actualizar el estado de una solicitud
    def cambiar_estado(self, colaborador_id, estado):
        """Devuelve cuántas filas cambió (0 si el id no existe)."""
        with self._transaccion() as cursor:
            cursor.execute("UPDATE Colaboradores SET estado = ? WHERE id = ?",
                           estado, colaborador_id)
            return cursor.rowcount

    # Esto sirve para: calcular los números del dashboard (por estado, país, área y recientes)
    def estadisticas(self):
        with self._conexion() as conexion:
            cursor = conexion.cursor()
            por_estado = {e: 0 for e in ESTADOS}
            cursor.execute("SELECT estado, COUNT(*) FROM Colaboradores GROUP BY estado")
            for estado, total in cursor.fetchall():
                por_estado[estado] = total

            cursor.execute("SELECT TOP 5 pais, COUNT(*) AS total FROM Colaboradores "
                           "GROUP BY pais ORDER BY total DESC, pais")
            por_pais = _a_dicts(cursor)

            cursor.execute("SELECT a.nombre, COUNT(ca.id) AS total "
                           "FROM AreasColaboracion a "
                           "LEFT JOIN ColaboradorAreas ca ON ca.area_id = a.id "
                           "GROUP BY a.id, a.nombre ORDER BY a.id")
            por_area = _a_dicts(cursor)

            cursor.execute("SELECT TOP 5 id, nombre_completo, pais, estado, fecha_registro "
                           "FROM Colaboradores ORDER BY fecha_registro DESC, id DESC")
            recientes = _a_dicts(cursor)

            return {"total": sum(por_estado.values()), "por_estado": por_estado,
                    "por_pais": por_pais, "por_area": por_area, "recientes": recientes}
