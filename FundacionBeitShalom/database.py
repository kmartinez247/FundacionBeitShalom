import pyodbc
from config import Config


# Esto sirve para: abrir una conexión a SQL Server con los datos del .env
def obtener_conexion():
    """Abre una conexión nueva a SQL Server con los datos del archivo .env"""
    partes = [
        f"DRIVER={{{Config.DB_DRIVER}}}",
        f"SERVER={Config.DB_SERVER}",
        f"DATABASE={Config.DB_NAME}",
        "Encrypt=yes",
        "TrustServerCertificate=yes",
    ]
    if Config.DB_USER:
        partes += [f"UID={Config.DB_USER}", f"PWD={Config.DB_PASSWORD}"]
    else:
        partes.append("Trusted_Connection=yes")
    return pyodbc.connect(";".join(partes) + ";")


# Esto sirve para: tener un nombre único para capturar errores de base de datos
ErrorBaseDatos = pyodbc.Error  # los controladores usan este nombre sin importar pyodbc
