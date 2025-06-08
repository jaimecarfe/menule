from src.modelo.dao.MenuDao import MenuDao

class LogicaMenu:
    def __init__(self):
        self.menu_dao = MenuDao()

    def obtener_menus_disponibles(self):
        return self.menu_dao.listar_disponibles()

    def obtener_menu_por_fecha(self, fecha: str):
        return self.menu_dao.obtener_platos_por_fecha(fecha)

    def obtener_id_menu_por_fecha(self, fecha: str):
        return self.menu_dao.obtener_id_menu_por_fecha(fecha)

    def insertar_o_modificar_menu(self, fecha: str, lista_platos_con_tipo: list[tuple[str, str]]) -> bool:
        return self.menu_dao.insertar_o_modificar_menu_con_tipo(fecha, lista_platos_con_tipo)

    def guardar_menu_con_alergenos(self, fecha: str, lista_platos: list[tuple[str, str, str]]) -> bool:
        return self.menu_dao.guardar_menu_con_alergenos(fecha, lista_platos)
