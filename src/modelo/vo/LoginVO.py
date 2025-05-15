class LoginVO:
    def __init__(self, nombre=None, correo=None, contrasena=None):
        # Puedes usar nombre o correo para identificar al usuario (según lógica)
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    def __repr__(self):
        return f"LoginVO(nombre={self.nombre}, correo={self.correo})"
