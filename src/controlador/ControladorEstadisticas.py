from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.EstadisticaVo import EstadisticaVo
class ControladorEstadisticas:
    def __init__(self, vista):
        self._vista = vista
        self._modelo = BussinessObject()
    
    def cargar_estadisticas(self, tipo):
        try:
            if tipo == 'Pagos':
                datos = self._modelo.estadistica_service.obtener_total_pagos_por_rol()
            elif tipo == 'Incidencias':
                datos = self._modelo.estadistica_service.obtener_estadisticas_incidencias()
            else:
                self._vista.mostrar_mensaje("Tipo de estadística no reconocido.")
                return

            vo = EstadisticaVo(tipo, datos)
            self._vista.mostrar_estadisticas(vo)

        except Exception as e:
            self._vista.mostrar_error(str(e))
