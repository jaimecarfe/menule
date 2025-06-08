class IncidenciaVo:
    def __init__(self, id=None, titulo=None, descripcion=None, fecha=None,
                 correo=None, estado="En proceso", numero_seguimiento=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.correo = correo
        self.estado = estado
        self.numero_seguimiento = numero_seguimiento
