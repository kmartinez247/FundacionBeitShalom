// Validaciones del navegador. Python vuelve a validar todo en el servidor.
document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formRegistro");
    if (!formulario) return;

    // Esto sirve para: guardar los campos del formulario que se van a validar
    const nombre = document.getElementById("nombre");
    const correo = document.getElementById("correo");
    const telefono = document.getElementById("telefono");
    const errorAreas = document.getElementById("errorAreas");
    const boton = formulario.querySelector(".btn-enviar");

    // Esto sirve para: revisar el formato de correo y teléfono (igual que en Python)
    const patronCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const patronTelefono = /^\+?[0-9\s()-]{7,30}$/;

    // Esto sirve para: saber si hay al menos un área marcada
    const hayAreas = () =>
        formulario.querySelectorAll('input[name="areas"]:checked').length > 0;

    // Esto sirve para: marcar cada campo como válido o con mensaje de error
    function revisarCampos() {
        nombre.setCustomValidity(
            nombre.value.trim().length < 5 ? "Ingresa tu nombre completo." : "");
        correo.setCustomValidity(
            patronCorreo.test(correo.value.trim())
                ? "" : "Ingresa un correo electrónico válido.");
        const tel = telefono.value.trim();
        telefono.setCustomValidity(
            tel === "" || patronTelefono.test(tel)
                ? "" : "Revisa el número de teléfono.");
    }

    // Esto sirve para: revalidar mientras la persona escribe
    // Se limpian los errores apenas la persona corrige el campo
    ["input", "change"].forEach((evento) =>
        formulario.addEventListener(evento, () => {
            revisarCampos();
            if (hayAreas()) errorAreas.textContent = "";
        }));

    // Esto sirve para: frenar el envío si hay errores y bloquear el botón al enviar
    formulario.addEventListener("submit", (e) => {
        revisarCampos();
        const areasOk = hayAreas();
        errorAreas.textContent = areasOk ? "" : "Selecciona al menos un área.";

        if (!areasOk || !formulario.checkValidity()) {
            e.preventDefault();
            if (formulario.checkValidity()) {
                errorAreas.scrollIntoView({ behavior: "smooth", block: "center" });
            } else {
                formulario.reportValidity();
            }
            return;
        }
        boton.disabled = true;
        (boton.querySelector("span") || boton).textContent = "Enviando...";
    });

    revisarCampos();
});
