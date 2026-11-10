# Pruebas manuales (con capturas)

Cada persona hace sus pruebas, toma captura y la nombra `prueba-N-descripcion.png`.
Las pruebas automáticas se corren con `python -m unittest discover -s tests -t . -v`.

## Formulario público

| N | Prueba | Resultado esperado | Responsable |
|---|---|---|---|
| 1 | Enviar el formulario vacío | Muestra los errores | 4 |
| 2 | Correo incorrecto (`hola`) | Rechaza el dato | 6 |
| 3 | No seleccionar áreas | Pide al menos una | 6 |
| 4 | No aceptar la privacidad | Impide el envío | 4 |
| 5 | Enviar datos correctos | Guarda y muestra la confirmación | 3 |
| 6 | Registrar un correo repetido | Avisa que ya existe | 2 |
| 7 | Consultar `Colaboradores` en SQL Server | Aparece el registro | 1 |
| 8 | Consultar `ColaboradorAreas` | Aparecen todas las áreas elegidas | 1 |
| 9 | Simular un error SQL | Se revierte la transacción (ver `tests/test_repositorios.py`) | 2 |
| 10 | Ver el formulario en celular | Se adapta a la pantalla | 5 |

## Panel administrativo y CRUD

| N | Prueba | Resultado esperado | Responsable |
|---|---|---|---|
| 11 | Entrar a `/admin/` sin iniciar sesión | Redirige al login | 3 |
| 12 | Login con contraseña mala | "Usuario o contraseña incorrectos" | 3 |
| 13 | Login correcto | Muestra el resumen | 3 |
| 14 | Buscar y filtrar en el listado | Muestra solo lo que coincide | 2 |
| 15 | Ver el detalle de una persona | Muestra todos sus datos y áreas | 4 |
| 16 | Editar datos y guardar | Los cambios se ven en el detalle | 2 |
| 17 | Editar con correo de otra persona | Avisa que ya existe | 2 |
| 18 | Aprobar y rechazar una solicitud | El estado cambia | 4 |
| 19 | Eliminar una solicitud | Desaparece del listado y de SQL Server | 1 |
| 20 | Exportar a Excel | Descarga un `.xlsx` con los datos | 6 |
| 21 | Cerrar sesión | Vuelve al login | 3 |
