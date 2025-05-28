from src.modelo.BussinessObject import BussinessObject

class ControladorEstadisticas:
    def __init__(self, vista):
        self._vista = vista
        self._modelo = BussinessObject()

    def cargar_estadisticas(self, tipo):
        try:
            estadistica_vo = self._modelo.obtenerEstadisticas(tipo)
            if not estadistica_vo.datos:
                self._vista.mostrar_mensaje("No hay datos disponibles para mostrar.")
            else:
                self._vista.mostrar_estadisticas(estadistica_vo)
        except Exception as e:
            self._vista.mostrar_error(f"No se pudieron recuperar los datos: {e}")