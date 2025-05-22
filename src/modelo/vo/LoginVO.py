class LoginVO:
    def __init__(self, correo, contrasena):
        self.correo = correo
        self.contrasena = contrasena

    def __repr__(self):
        return f"LoginVO(correo={self.correo})"
