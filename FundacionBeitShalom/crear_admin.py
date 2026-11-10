"""Crea una cuenta de administrador. Uso:  python crear_admin.py"""
import re
from getpass import getpass

from werkzeug.security import generate_password_hash

from repositories.administrador_repository import AdministradorRepository


# Esto sirve para: crear un administrador desde la consola, validando usuario y contraseña
def main():
    usuario = input("Usuario (letras, números, _ . -): ").strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,50}", usuario):
        print("Usuario no válido: usa de 3 a 50 caracteres, sin espacios.")
        return
    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("El nombre es obligatorio.")
        return

    while True:
        clave = getpass("Contraseña (mínimo 8 caracteres): ")
        if len(clave) < 8:
            print("Es muy corta, intenta de nuevo.")
        elif clave != getpass("Repite la contraseña: "):
            print("No coinciden, intenta de nuevo.")
        else:
            break

    try:
        AdministradorRepository().crear(usuario, nombre[:100], generate_password_hash(clave))
        print(f"Listo. Ya puedes entrar con el usuario «{usuario}».")
    except Exception as error:
        if "UQ_Administradores_Usuario" in str(error):
            print("Ese usuario ya existe.")
        elif "Administradores" in str(error):
            print("Falta la tabla. Ejecuta primero sql/panel_admin.sql en SQL Server.")
        else:
            print("No se pudo crear el usuario:", error)


if __name__ == "__main__":
    main()
