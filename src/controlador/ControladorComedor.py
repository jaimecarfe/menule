from modelo.BussinessObject import BussinessObject
from modelo.vo.UserVo import UserVo
from modelo.vo.MenuVo import MenuVo
from modelo.vo.ReservaVo import ReservaVo
from modelo.vo.TicketVo import TicketVo
from modelo.vo.PlatoVo import PlatoVo
from modelo.vo.IngredienteVo import IngredienteVo


class ControladorComedor:
    def __init__(self, usuario_actual):
        self._usuario = usuario_actual
        self._modelo = BussinessObject()

    def procesar_ticket(self, codigo_qr):
        pass

    def consultar_reservas_por_plato(self, id_menu):
        pass

    def ver_stock(self):
        pass