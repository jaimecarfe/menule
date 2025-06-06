from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.MenuVo import MenuVo
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.TicketVo import TicketVo
#from src.modelo.vo.PlatoVo import PlatoVo
#from src.modelo.vo.IngredienteVo import IngredienteVo


class ControladorComedor:
    def __init__(self, usuario_actual):
        self._usuario = usuario_actual
        self._modelo = BussinessObject()
        self.bo = BussinessObject()

    def procesar_ticket(self, codigo_qr):
        pass

    def consultar_reservas_por_plato(self, id_menu):
        pass

    def ver_stock(self):
        pass

    def obtener_reservas(self):
        return self._modelo.get_reservas_completas()
    
    def reportar_incidencia(self, incidenciaVo):
        self.bo.registrar_incidencia(incidenciaVo)
