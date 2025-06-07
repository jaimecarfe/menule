from src.modelo.BussinessObject import BussinessObject

class ControladorMenus:
    def __init__(self):
        self._modelo = BussinessObject()

    def obtener_menus_disponibles(self):
        return self._modelo.menu_service.obtener_menus_disponibles()

    def obtener_menu_por_fecha(self, fecha: str):
        return self._modelo.menu_service.obtener_menu_por_fecha(fecha)

    def obtener_id_menu_por_fecha(self, fecha: str):
        return self._modelo.menu_service.obtener_id_menu_por_fecha(fecha)

    def insertar_o_modificar_menu(self, fecha: str, lista_platos_con_tipo: list[tuple[str, str]]):
        return self._modelo.menu_service.insertar_o_modificar_menu(fecha, lista_platos_con_tipo)

    def guardar_menu_con_alergenos(self, fecha: str, lista_platos: list[tuple[str, str, str]]):
        return self._modelo.menu_service.guardar_menu_con_alergenos(fecha, lista_platos)
