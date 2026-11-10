# Fundación Beit Shalom – Sistema de Registro de Colaboradores

Aplicación web para que las personas que quieren apoyar a la Fundación envíen su solicitud
(formulario público) y para que el personal las consulte, edite, apruebe, elimine y
exporte a Excel (panel administrativo).

**Tecnologías:** Python 3 · Flask · POO · patrón MVC con capa Repository · SQL Server ·
pyodbc · HTML5 · CSS3 (plantilla Kidearn con Bootstrap) · JavaScript · openpyxl (Excel) · unittest (pruebas).

## Requisitos

- Python 3.10 o superior.
- SQL Server (con autenticación de SQL Server si usas usuario y contraseña) y SQL Server Management Studio.
- **ODBC Driver 18 for SQL Server** instalado.
- Git (para trabajar en equipo).

## Instalación paso a paso

1. Clonar el repositorio y entrar a la carpeta del proyecto.
2. Crear la base de datos (ver "Scripts SQL").
3. Crear tu archivo `.env`: copiar `.env.example` como `.env` y llenar tus datos.
4. En la terminal, dentro del proyecto:

   ```
   python -m venv venv
   .\venv\Scripts\Activate
   pip install -r requirements.txt
   python crear_admin.py
   python app.py
   ```
5. Abrir `http://127.0.0.1:5000` (sitio de la Fundación), `/registro` (formulario) o `/admin/login` (panel).

## Variables de entorno (`.env`)

| Variable | Para qué sirve | Ejemplo |
|---|---|---|
| `SECRET_KEY` | Protege las sesiones y los formularios. Usa un texto largo y secreto. | `beitshalom-clave-2026` |
| `FLASK_DEBUG` | `1` en desarrollo, `0` al publicar. | `1` |
| `DB_DRIVER` | Driver ODBC instalado. | `ODBC Driver 18 for SQL Server` |
| `DB_SERVER` | Nombre del servidor SQL Server. | `localhost` o `PC\SQLEXPRESS` |
| `DB_NAME` | Nombre de la base de datos. | `BeitShalomDB` |
| `DB_USER` | Usuario de SQL Server. Vacío = autenticación de Windows. | `sa` |
| `DB_PASSWORD` | Contraseña de ese usuario. | (la tuya) |
| `SESSION_COOKIE_SECURE` | `1` solo cuando se publique con HTTPS. | `0` |

El archivo `.env` **nunca** se sube a GitHub (está en `.gitignore`).

## Scripts SQL (ejecutar en este orden)

1. `sql/crear_base_datos.sql`: crea `BeitShalomDB` y las tablas `Colaboradores`, `AreasColaboracion` y `ColaboradorAreas`.
2. `sql/panel_admin.sql`: crea la tabla `Administradores`.
3. `sql/datos_prueba.sql` (opcional): carga 16 solicitudes de ejemplo.

Después se crea la cuenta del panel con `python crear_admin.py`. La contraseña se guarda con hash.

## Estructura del proyecto

```
FundacionBeitShalom
├── app.py                     Inicia Flask y registra los controladores
├── config.py                  Configuración (lee el .env)
├── database.py                Conexión a SQL Server
├── crear_admin.py             Crea cuentas del panel
├── requirements.txt
├── models/                    MODELO: clases y reglas de negocio
│   ├── persona.py             Clase padre
│   ├── colaborador.py         Hereda de Persona
│   └── administrador.py       Hereda de Persona
├── repositories/              Todo el SQL
│   ├── base_repository.py     Clase padre (conexión y transacciones)
│   ├── colaborador_repository.py
│   ├── panel_repository.py
│   └── administrador_repository.py
├── controllers/               CONTROLADOR: reciben peticiones y coordinan
│   ├── sitio_controller.py    Páginas del sitio (inicio, nosotros, etc.)
│   ├── colaborador_controller.py
│   └── admin_controller.py
├── servicios/exportador_excel.py
├── templates/                 VISTA: base.html (encabezado y pie del sitio), sitio/, formulario y admin/
├── static/                    Plantilla Kidearn: css, js, images y vendors
├── sql/                       Scripts de base de datos
├── tests/                     Pruebas automáticas
└── docs/                      Guía de GitHub, pruebas y sustentación
```

## Sitio web de la Fundación

El sitio (inicio, nosotros, programas, proyectos, eventos, galería, noticias y contacto) usa la
plantilla Kidearn adaptada a Beit Shalom, y ahora lo sirve Flask:

- El encabezado, el menú y el pie de página están **una sola vez** en `templates/base.html`.
- El contenido de cada página está en `templates/sitio/` (ahí se cambian los textos).
- Los colores propios de la Fundación están en `static/css/beit-shalom.css`.
- El formulario de colaboradores (`/registro`) y el panel (`/admin`) se integran al menú ("Colaborar").
- El formulario de la página Contacto aún apunta a `sendemail.php`, que Flask no ejecuta.

## Arquitectura

- **Vista:** `templates/` y `static/`. Solo muestra datos y recoge formularios.
- **Controlador:** `controllers/`. Recibe la petición, valida con el modelo y llama al repository. No contiene SQL.
- **Modelo:** `models/`. Clases con sus reglas (por ejemplo `Colaborador.validar()`).
- **Repository:** `repositories/`. Único lugar con consultas SQL, siempre con parámetros.

## Programación orientada a objetos

- **Clases y objetos:** `Colaborador`, `Administrador` y los repositories.
- **Herencia:** `Colaborador` y `Administrador` heredan de `Persona`. Los tres repositories heredan de `BaseRepository`.
- **Encapsulamiento:** atributos privados (`_correo`, `_password_hash`) con `@property` y setters que limpian los datos.
- **Polimorfismo:** `__str__` se redefine en `Colaborador`.

## CRUD

| Operación | Dónde | Código |
|---|---|---|
| Crear | Formulario público `/registro` | `ColaboradorRepository.guardar` |
| Leer | `/admin/colaboradores` y su detalle | `PanelRepository.listar` y `detalle` |
| Actualizar | `/admin/colaboradores/<id>/editar` y cambio de estado | `ColaboradorRepository.actualizar`, `PanelRepository.cambiar_estado` |
| Eliminar | Botón en el detalle | `ColaboradorRepository.eliminar` |

## Validaciones y errores

- JavaScript valida en el navegador y Python vuelve a validar en el servidor.
- Consultas con parámetros (contra inyección SQL), formularios con token CSRF y sesiones con tiempo límite.
- Las escrituras usan transacciones: si algo falla se hace rollback.
- Páginas amigables para errores 404, 405, 500 y para fallos de base de datos.

## Pruebas automáticas

```
python -m unittest discover -s tests -t . -v
```

Las pruebas no necesitan SQL Server: usan objetos falsos. Las pruebas manuales con capturas están en `docs/PRUEBAS.md`.

## Trabajo en equipo (GitHub)

Ramas por parte y pull requests: ver `docs/GUIA_GITHUB.md`.

## Antes de publicar

`FLASK_DEBUG=0`, una `SECRET_KEY` larga y secreta, `SESSION_COOKIE_SECURE=1`, HTTPS y un
servidor de producción (por ejemplo waitress) en lugar de `python app.py`.

## Integrantes

(Completar con los nombres del equipo y la parte de cada uno.)
