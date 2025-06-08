class TicketVo:
    def __init__(self, id_ticket=None, id_reserva=None, codigo=None, fecha_generacion=None, estado=None, fecha_uso=None):
        self.id_ticket = id_ticket
        self.id_reserva = id_reserva
        self.codigo = codigo
        self.fecha_generacion = fecha_generacion
        self.estado = estado
        self.fecha_uso = fecha_uso