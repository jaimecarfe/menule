class ReservaVo:
    def __init__(self, id_reserva=None, id_usuario=None, id_menu=None, fecha_reserva=None, estado=None, fecha_cancelacion=None, motivo_cancelacion=None):
        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.id_menu = id_menu
        self.fecha_reserva = fecha_reserva
        self.estado = estado
        self.fecha_cancelacion = fecha_cancelacion
        self.motivo_cancelacion = motivo_cancelacion