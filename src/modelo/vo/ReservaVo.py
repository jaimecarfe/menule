class ReservaVo:
    def __init__(self, id_reserva=None, id_usuario=None, id_menu=None, fecha_reserva=None, estado=None, estado_bit=None):
        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.id_menu = id_menu
        self.fecha_reserva = fecha_reserva
        self.estado = estado
        self.estado_bit = estado_bit
