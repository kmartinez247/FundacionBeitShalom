# Guía para la sustentación

Cada integrante debe poder abrir su parte y explicarla con sus propias palabras.

## Dónde se ve cada criterio de la rúbrica

| Criterio | Dónde mostrarlo |
|---|---|
| Arquitectura MVC | `controllers/` (sin SQL), `repositories/` (todo el SQL), `models/`, `templates/` |
| POO | `models/persona.py`, `colaborador.py`, `administrador.py`, `repositories/base_repository.py` |
| SQL Server | `sql/crear_base_datos.sql` (PK, FK, UNIQUE, CHECK) y consultas con parámetros |
| CRUD | Tabla "CRUD" del README |
| Calidad de código | Docstrings, nombres claros, `servicios/` separado, `.flake8` |
| Errores y validaciones | `validar()`, `validaciones.js`, transacciones, páginas de error |
| GitHub | Ramas por parte y pull requests (`docs/GUIA_GITHUB.md`) |
| Interfaz | Formulario, panel, diseño adaptable a celular |
| README | `README.md` |

## Preguntas probables por parte

**1. Base de datos**
- ¿Por qué tres tablas? Porque una persona elige varias áreas y cada área la eligen muchas personas (relación muchos a muchos).
- ¿Para qué sirven las llaves foráneas? Para que no exista un área o una persona que no existe.
- ¿Por qué el correo es único? Para no registrar dos veces a la misma persona.
- ¿Qué pasa al eliminar? Se borran primero las áreas de la persona y luego la persona, porque la tabla hija depende de la principal.

**2. Modelo y Repository**
- ¿Qué es herencia y dónde la usan? `Colaborador` y `Administrador` heredan de `Persona`; los repositories heredan de `BaseRepository`.
- ¿Qué es el encapsulamiento? Guardar los datos privados (`_correo`) y usarlos con `@property`, así siempre se limpian al asignarlos.
- ¿Por qué un Repository? Para que el SQL esté en un solo lugar y los controladores no lo tengan.
- ¿Qué es una transacción? Varias operaciones que se guardan juntas o no se guarda ninguna (commit o rollback).
- ¿Por qué consultas con parámetros (`?`)? Para evitar la inyección SQL.

**3. Controlador e integración**
- ¿Qué hace el controlador? Recibe la petición, valida y le pide al repository que guarde.
- ¿Qué es un Blueprint? Una forma de separar las rutas en módulos (público y administrativo).
- ¿Qué es CSRF? Un ataque que envía formularios en nombre del usuario; el token lo evita.
- ¿Cómo protegen el panel? Con login, sesión con tiempo límite y un decorador que revisa la sesión en cada ruta.
- ¿Por qué hash para las contraseñas? Para no guardar la contraseña real: aunque roben la base, no la ven.

**4. HTML**
- ¿Para qué sirve `name` en cada campo? Es el nombre con el que Python recibe el dato.
- ¿Qué es Jinja2 y `{% extends %}`? El motor de plantillas de Flask; permite reutilizar `base.html`.
- ¿Qué atributos de validación usaron? `required`, `type="email"`, `minlength`, `maxlength`.

**5. CSS**
- ¿Cómo se adapta a celular? Con una media query (`max-width: 600px`) que pasa las columnas a una sola.
- ¿Qué es Grid o Flexbox? Formas de acomodar elementos en filas y columnas.
- ¿Cómo muestran los estados de cada solicitud? Con clases de color (`estado-aprobado`, etc.).

**6. JavaScript y pruebas**
- ¿Por qué validan también en Python? Porque alguien puede saltarse el JavaScript y enviar datos directo.
- ¿Qué hace `setCustomValidity`? Pone un mensaje de error propio en un campo.
- ¿Qué pruebas hicieron? Las manuales de `docs/PRUEBAS.md` y las automáticas con `unittest`.
- ¿Por qué las pruebas automáticas no necesitan SQL Server? Usan objetos falsos que hacen de repository.

## Preguntas para todos

- ¿Qué es MVC y cómo se ve en el proyecto?
- Sigan el recorrido completo de una solicitud, desde el formulario hasta SQL Server.
- ¿Qué cambiarían para publicarlo?
