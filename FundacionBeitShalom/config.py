import os
from dotenv import load_dotenv

# Esto sirve para: leer las variables del archivo .env
load_dotenv()


# Esto sirve para: guardar la configuración (clave secreta, base de datos, cookies)
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "cambiar-esta-clave-en-produccion")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    DB_SERVER = os.getenv("DB_SERVER", "localhost")
    DB_NAME = os.getenv("DB_NAME", "BeitShalomDB")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
