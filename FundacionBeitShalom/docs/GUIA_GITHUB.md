# Guía de GitHub para el equipo

La rúbrica evalúa tres cosas: la **estructura del repositorio**, que el **flujo de trabajo sea
ordenado** y que **no falten archivos indispensables**. Esta guía cubre las tres.

## 1. Archivos que deben estar en el repositorio

| Archivo o carpeta | Debe estar | Nota |
|---|---|---|
| `README.md` | Sí | Instalación, variables, scripts SQL |
| `requirements.txt` | Sí | Las dependencias |
| `.gitignore` | Sí | Deja fuera `venv/`, `.env` y `__pycache__/` |
| `.env.example` | Sí | Modelo del `.env` sin contraseñas |
| `sql/` | Sí | Los 3 scripts |
| `app.py`, `models/`, `repositories/`, `controllers/`, `templates/`, `static/`, `tests/`, `docs/` | Sí | El código |
| `.env` | **No** | Tiene tu contraseña |
| `venv/` | **No** | Cada quien crea el suyo |

## 2. Primera subida (la hace la persona integradora, una sola vez)

1. En GitHub: **New repository**, nombre `FundacionBeitShalom`, sin README ni .gitignore.
2. Invitar a los 5 compañeros en Settings > Collaborators.
3. En la terminal, dentro de la carpeta del proyecto:

```
git init
git add .
git status
git commit -m "Proyecto base: registro público y panel administrativo"
git branch -M main
git remote add origin https://github.com/USUARIO/FundacionBeitShalom.git
git push -u origin main
```

Antes del `commit`, `git status` no debe mostrar `.env` ni `venv`.

## 3. Flujo de trabajo del equipo

- `main` es la rama estable: **nadie sube directo a main**.
- Cada persona trabaja en **su propia rama**, con el nombre de su parte.
- Los cambios entran a `main` con un **Pull Request** que revisa la persona integradora.

| Persona | Rama |
|---|---|
| 1. Base de datos | `feature/base-de-datos` |
| 2. Modelo y Repository | `feature/modelo-repository` |
| 3. Controlador e integración | `feature/controlador` |
| 4. HTML | `feature/html` |
| 5. CSS | `feature/css` |
| 6. JavaScript y pruebas | `feature/javascript-pruebas` |

### Pasos para cada integrante

```
git clone https://github.com/USUARIO/FundacionBeitShalom.git
cd FundacionBeitShalom
git checkout -b feature/html
```

Trabajas en tus archivos y, cuando tengas un avance:

```
git add templates/registro.html
git commit -m "Agrego el logo de la Fundación al encabezado del formulario"
git push -u origin feature/html
```

Luego, en GitHub: **Compare & pull request** > escribir qué cambiaste > **Create pull request**.

La persona integradora revisa los cambios, prueba que el sistema corra y presiona **Merge pull request**.

Antes de empezar un trabajo nuevo, actualiza tu copia:

```
git checkout main
git pull
git checkout -b feature/nombre-del-trabajo
```

## 4. Mensajes de commit

Cortos y que digan qué se hizo: "Agrego validación del teléfono en JavaScript", "Corrijo el color del botón en celular". Evita "update" o "fix".

## 5. Si hay conflictos

Pasa cuando dos personas cambian el mismo archivo. Por eso cada quien toca solo sus archivos. Si pasa, avisen al grupo y resuelvan juntos antes de hacer el merge.
