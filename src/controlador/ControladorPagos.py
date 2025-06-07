from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.PagoVo import PagoVo
from datetime import datetime

class ControladorPagos:
    def __init__(self):
        self._modelo = BussinessObject()

    def registrar_pago(self, pago_vo: PagoVo) -> int | None:
        return self._modelo.pago_service.registrar_pago(pago_vo)

    def obtener_pagos_usuario(self, id_usuario: int):
        return self._modelo.pago_service.obtener_pagos_por_usuario(id_usuario)

    def obtener_todos_los_pagos(self):
        return self._modelo.pago_service.obtener_todos_los_pagos()

    def pagar_con_tui(self, usuario, monto, id_reserva):
        saldo_actual = self._modelo.usuario_service.obtener_saldo(usuario.idUser)
        if saldo_actual < monto:
            return False, "Saldo insuficiente"

        self._modelo.usuario_service.actualizar_saldo(usuario.idUser, saldo_actual - monto)

        pago = PagoVo(
            id_pago=None,
            id_usuario=usuario.idUser,
            metodo="tui",
            monto=monto,
            fecha_pago=datetime.now(),
            id_reserva=id_reserva
        )
        pago_id = self.registrar_pago(pago)
        return pago_id is not None, "Pago registrado correctamente" if pago_id else "Error al registrar el pago"

    def pagar_con_tarjeta(self, monto, id_reserva, id_usuario=0):
        pago = PagoVo(
            id_pago=None,
            id_usuario=id_usuario,
            metodo="tarjeta",
            monto=monto,
            fecha_pago=datetime.now(),
            id_reserva=id_reserva,
        )
        pago_id = self.registrar_pago(pago)
        return pago_id is not None, "Pago registrado correctamente" if pago_id else "Error al registrar el pago"
