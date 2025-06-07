from src.modelo.dao.PagoDao import PagoDao
from src.modelo.vo.PagoVo import PagoVo

class LogicaPago:
    def __init__(self):
        self.pago_dao = PagoDao()

    def registrar_pago(self, pago_vo: PagoVo) -> int | None:
        return self.pago_dao.insertar_pago(pago_vo)

    def obtener_pagos_por_usuario(self, id_usuario: int):
        return self.pago_dao.obtener_por_usuario(id_usuario)

    def obtener_todos_los_pagos(self):
        return self.pago_dao.obtener_todos_pagos()
