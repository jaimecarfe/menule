from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.UserVo import UserVo
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.MenuVo import MenuVo


class ControladorProfesor:
    def __init__(self, usuario_actual):
        self._usuario = usuario_actual
        self._modelo = BussinessObject()

    def hacer_reserva(self, id_menu, fecha):
        pass

    def ver_historial_reservas(self):
        pass