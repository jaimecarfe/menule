from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.MenuVo import MenuVo
from src.modelo.vo.UserVo import UseroVo
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.PlatoVo import PlatoVo
from src.modelo.vo.IncidenciaVo import IncidenciaVo



class ControladorAdmin:
    def __init__(self, usuario_actual):
        self._usuario = usuario_actual
        self._modelo = BussinessObject()

    def crear_usuario(self, userVO):
        pass

    def listar_usuarios(self):
        pass

    def eliminar_usuario(self, id_usuario):
        pass

    def crear_menu(self, menuVO):
        pass

    def modificar_plato(self, platoVO):
        pass

    def ver_estadisticas(self):
        pass

    def ver_incidencias(self):
        pass

    def resolver_incidencia(self, id_incidencia, solucion):
        pass