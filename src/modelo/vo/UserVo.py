class UserVo:
    def __init__(self, idUser, nombre, apellido, correo, contrasena, rol=None, saldo=0.0, tui=None):
        self.idUser = idUser
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol                # 'estudiante', 'personal', 'visitante', etc.
        self.saldo = saldo            # saldo recargable para pagos
        self.tui = tui                # ID de la Tarjeta Universitaria ULE (si la tiene)
