# src/modelo/logica/LogicaMenu.py
from src.modelo.dao.MenuDao import MenuDao
from datetime import datetime, date

class LogicaMenu:
    def __init__(self):
        self.menu_dao = MenuDao()

    def _normalizar_fecha(self, fecha_input) -> str:
        """Helper para asegurar que cualquier entrada de fecha termine como string YYYY-MM-DD."""
        if isinstance(fecha_input, (datetime, date)):
            return fecha_input.strftime('%Y-%m-%d')
        
        # Si viene de PyQt como objeto QDate, tendrá el método toPyDate() o toString()
        if hasattr(fecha_input, 'toPyDate'):
            return fecha_input.toPyDate().strftime('%Y-%m-%d')
        elif hasattr(fecha_input, 'toString'):
            # Formato Qt ISO: YYYY-MM-DD
            return fecha_input.toString("yyyy-MM-dd")
            
        # Si ya es un string, lo limpiamos de espacios u horas sobrantes
        fecha_str = str(fecha_input).strip()
        if " " in fecha_str:
            fecha_str = fecha_str.split(" ")[0]
        return fecha_str

    def obtener_menus_disponibles(self):
        return self.menu_dao.listar_disponibles()

    def obtener_menu_por_fecha(self, fecha):
        fecha_limpia = self._normalizar_fecha(fecha)
        return self.menu_dao.obtener_platos_por_fecha(fecha_limpia)

    def obtener_id_menu_por_fecha(self, fecha):
        fecha_limpia = self._normalizar_fecha(fecha)
        return self.menu_dao.obtener_id_menu_por_fecha(fecha_limpia)

    def insertar_o_modificar_menu(self, fecha, lista_platos_con_tipo: list[tuple[str, str]]) -> bool:
        fecha_limpia = self._normalizar_fecha(fecha)
        return self.menu_dao.insertar_o_modificar_menu_con_tipo(fecha_limpia, lista_platos_con_tipo)

    def guardar_menu_con_alergenos(self, fecha, lista_platos: list[tuple[str, str, str]]) -> bool:
        fecha_limpia = self._normalizar_fecha(fecha)
        return self.menu_dao.guardar_menu_con_alergenos(fecha_limpia, lista_platos)