import re

from models.persona import Persona

# Esto sirve para: definir las opciones válidas de los listados desplegables
PAISES = [
    "El Salvador", "Guatemala", "Honduras", "Nicaragua", "Costa Rica",
    "Panamá", "México", "Colombia", "Venezuela", "Ecuador", "Perú",
    "Bolivia", "Chile", "Argentina", "Uruguay", "Paraguay", "Brasil",
    "República Dominicana", "Estados Unidos", "España", "Otro",
]
MODALIDADES = ["Presencial", "Virtual", "Ambas"]
DISPONIBILIDADES = ["Entre semana", "Fines de semana", "Horarios flexibles", "Ocasional"]
ESTADOS = ["Pendiente", "En revisión", "Aprobado", "Rechazado"]

# Esto sirve para: validar el formato de correo y teléfono
_CORREO = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_TELEFONO = re.compile(r"^\+?[0-9\s()-]{7,30}$")


# Esto sirve para: quitar espacios y convertir None en texto vacío
def _limpiar(valor):
    """Convierte None en texto vacío y quita los espacios de los extremos."""
    return (valor or "").strip()


# Esto sirve para: representar una solicitud de colaboración y validarla
class Colaborador(Persona):
    """Una solicitud de colaboración. Hereda el nombre de Persona.

    Los atributos son privados (_pais, _correo...) y se usan mediante
    propiedades: así cada valor se limpia siempre que se asigna (encapsulamiento).
    """

    def __init__(self, nombre, pais, correo, telefono,
                 modalidad, disponibilidad, motivacion):
        super().__init__(nombre)
        self.pais = pais
        self.correo = correo
        self.telefono = telefono
        self.modalidad = modalidad
        self.disponibilidad = disponibilidad
        self.motivacion = motivacion

    # Esto sirve para: crear un Colaborador directamente desde los datos del formulario
    @classmethod
    def desde_formulario(cls, formulario):
        """Crea un Colaborador a partir de request.form (o cualquier dict)."""
        return cls(
            nombre=formulario.get("nombre", ""),
            pais=formulario.get("pais", ""),
            correo=formulario.get("correo", ""),
            telefono=formulario.get("telefono", ""),
            modalidad=formulario.get("modalidad", ""),
            disponibilidad=formulario.get("disponibilidad", ""),
            motivacion=formulario.get("motivacion", ""),
        )

    @property
    def pais(self):
        return self._pais

    @pais.setter
    def pais(self, valor):
        self._pais = _limpiar(valor)

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = _limpiar(valor)

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = _limpiar(valor)

    @property
    def modalidad(self):
        return self._modalidad

    @modalidad.setter
    def modalidad(self, valor):
        self._modalidad = _limpiar(valor)

    @property
    def disponibilidad(self):
        return self._disponibilidad

    @disponibilidad.setter
    def disponibilidad(self, valor):
        self._disponibilidad = _limpiar(valor)

    @property
    def motivacion(self):
        return self._motivacion

    @motivacion.setter
    def motivacion(self, valor):
        self._motivacion = _limpiar(valor)

    # Esto sirve para: revisar todos los campos y devolver la lista de errores
    def validar(self):
        """Devuelve una lista de errores. Si está vacía, los datos son válidos."""
        errores = []
        if not 5 <= len(self.nombre) <= 150:
            errores.append("El nombre completo debe tener entre 5 y 150 caracteres.")
        if self.pais not in PAISES:
            errores.append("Debes seleccionar un país.")
        if not _CORREO.match(self.correo) or len(self.correo) > 150:
            errores.append("El correo no es válido.")
        if self.telefono and not _TELEFONO.match(self.telefono):
            errores.append("El teléfono no es válido.")
        if self.modalidad not in MODALIDADES:
            errores.append("La modalidad no es válida.")
        if self.disponibilidad not in DISPONIBILIDADES:
            errores.append("La disponibilidad no es válida.")
        if len(self.motivacion) > 1000:
            errores.append("La motivación no puede superar los 1000 caracteres.")
        return errores

    # Esto sirve para: mostrar al colaborador como «Nombre <correo>»
    def __str__(self):
        # Polimorfismo: mismo método que Persona, pero con otro resultado
        return f"{self.nombre} <{self.correo}>"
