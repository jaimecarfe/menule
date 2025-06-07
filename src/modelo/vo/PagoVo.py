class PagoVo:
    def __init__(self, id_pago=None, id_usuario=None, id_reserva=None, monto=None, metodo=None, fecha_pago=None, descuento=None, estado=None, transaccion_id=None, correo=None):
        self.id_pago = id_pago
        self.id_usuario = id_usuario
        self.id_reserva = id_reserva
        self.monto = monto
        self.metodo = metodo
        self.fecha_pago = fecha_pago
        self.descuento = descuento
        self.estado = estado
        self.transaccion_id = transaccion_id
        self.correo = correo