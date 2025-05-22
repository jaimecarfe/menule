from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.MenuVo import MenuVo
from src.modelo.vo.TicketVo import TicketVo

class ControladorVisitante:
    def __init__(self):
        self._modelo = BussinessObject()

    def hacer_reserva_anonima(self, nombre, correo, platos):
        pass

    def enviar_ticket_email(self, correo, codigo_ticket):
        pass