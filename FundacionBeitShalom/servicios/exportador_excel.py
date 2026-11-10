from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

# Esto sirve para: definir los títulos y anchos de columna del Excel
ENCABEZADOS = ["ID", "Nombre completo", "País", "Correo", "Teléfono", "Modalidad",
               "Disponibilidad", "Áreas de colaboración", "Estado", "Fecha de registro"]
ANCHOS = [6, 30, 18, 32, 18, 14, 20, 45, 14, 18]


# Esto sirve para: evitar que un texto que empieza con '=' se ejecute como fórmula
def _seguro(valor):
    """Evita que un texto escrito por el público se guarde como fórmula en Excel."""
    texto = "" if valor is None else str(valor)
    return "'" + texto if texto.startswith("=") else texto


# Esto sirve para: generar el archivo .xlsx con las solicitudes
def crear_excel(filas):
    """Recibe la lista de colaboradores y devuelve el archivo .xlsx en memoria."""
    libro = Workbook()
    hoja = libro.active
    hoja.title = "Colaboradores"
    hoja.append(ENCABEZADOS)
    for celda in hoja[1]:
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill("solid", fgColor="173B5E")
    for f in filas:
        hoja.append([
            f["id"], _seguro(f["nombre_completo"]), _seguro(f["pais"]),
            _seguro(f["correo"]), _seguro(f["telefono"]), f["modalidad"],
            f["disponibilidad"], _seguro(", ".join(f["areas"])), f["estado"],
            f["fecha_registro"].strftime("%Y-%m-%d %H:%M"),
        ])
    for columna, ancho in zip("ABCDEFGHIJ", ANCHOS):
        hoja.column_dimensions[columna].width = ancho
    hoja.freeze_panes = "A2"
    hoja.auto_filter.ref = hoja.dimensions
    salida = BytesIO()
    libro.save(salida)
    salida.seek(0)
    return salida
