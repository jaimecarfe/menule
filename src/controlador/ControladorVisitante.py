from src.modelo.BussinessObject import BussinessObject
"""
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.MenuVo import MenuVo
from src.modelo.vo.TicketVo import TicketVo
"""

class ControladorVisitante:
    def __init__(self):
        self._modelo = BussinessObject()

    def hacer_reserva_anonima(self, fecha, primero, segundo, postre):
        return self._modelo.crearReservaAnonima(fecha, primero, segundo, postre)

    def obtener_ultima_reserva_id(self, id_usuario):
        return self._modelo.obtenerUltimaReservaId(id_usuario)

    def enviar_ticket_email(self, correo, codigo_ticket):
        pass