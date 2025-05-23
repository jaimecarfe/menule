class UserVo:
    def __init__(self, idUser, nombre, apellido, correo, contrasena, rol, saldo=0.0,
                 tui=None, dni=None, telefono=None, fecha_alta=None, activo=True,
                 grado_academico=None, especialidad=None):
        self.idUser = idUser
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol
        self.saldo = saldo
        self.tui = tui
        self.dni = dni
        self.telefono = telefono
        self.fecha_alta = fecha_alta
        self.activo = activo
        self.grado_academico = grado_academico
        self.especialidad = especialidad
