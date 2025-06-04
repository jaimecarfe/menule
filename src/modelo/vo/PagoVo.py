class PagoVo:
    def __init__(self, id_pago=None, id_usuario=None, id_pedido=None, monto=None, fecha_pago=None, descuento=None, estado=None, transaccion_id=None):
        self.id_pago = id_pago
        self.id_usuario = id_usuario
        self.id_pedido = id_pedido
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.descuento = descuento
        self.estado = estado
        self.transaccion_id = transaccion_id
