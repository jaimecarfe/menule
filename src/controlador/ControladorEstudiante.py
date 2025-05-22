from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.vo.MenuVo import MenuVo
from src.modelo.vo.UserVo import UseroVo

class ControladorEstudiante:
    def __init__(self, usuario_actual):
        self._usuario = usuario_actual
        self._modelo = BussinessObject()

    def hacer_reserva(self, id_menu, fecha):
        pass

    def cancelar_reserva(self, id_reserva, motivo):
        pass

    def ver_historial_reservas(self):
        pass

    def reportar_incidencia(self, titulo, descripcion):
        pass
