# src/modelo/logica/LogicaPago.py
from src.modelo.dao.PagoDao import PagoDao
from src.modelo.vo.PagoVo import PagoVo
from src.modelo.dao.UserDao import UserDao # Importamos el DAO de usuario para proteger el saldo

class LogicaPago:
    def __init__(self):
        self.pago_dao = PagoDao()
        self.user_dao = UserDao()

    def registrar_pago(self, pago_vo: PagoVo) -> int | None:
        """
        Registra el pago de manera segura. Si es un pago por saldo (TUI), 
        valida y asienta el registro antes de alterar de forma irreversible el monedero.
        """
        # 1. Intentamos insertar el registro en la tabla Pagos primero
        id_pago = self.pago_dao.insertar_pago(pago_vo)
        
        # 2. Si la inserción falló por tipos o base de datos, abortamos de inmediato
        if not id_pago:
            print("⚠️ Operación de pago cancelada en la capa de lógica debido a un fallo en el DAO.")
            return None
            
        return id_pago

    def obtener_pagos_por_usuario(self, id_usuario: int):
        return self.pago_dao.obtener_por_usuario(id_usuario)

    def obtener_todos_los_pagos(self):
        return self.pago_dao.obtener_todos_pagos()