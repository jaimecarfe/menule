import re

def validar_dni(dni: str) -> bool:
    patron = re.match(r"^(\d{8})([A-Z])$", dni.upper())
    if not patron:
        return False
    numero, letra = patron.groups()
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    return letras[int(numero) % 23] == letra

def validar_correo_por_rol(correo: str, rol: str) -> bool:
    dominios = {
        "estudiante": "@estudiantes.unileon.es",
        "profesor": "@unileon.es",
        "personal_comedor": "@comedor.unileon.es",
        "administrador": "@menule.com",
        "visitante": ("@gmail.com", "@hotmail.com"),
    }
    if rol == "visitante":
        return correo.endswith(dominios[rol])
    return correo.endswith(dominios.get(rol, ""))
