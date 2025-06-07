from src.modelo.dao.EstadisticaDao import EstadisticaDao
from src.modelo.vo.EstadisticaVo import EstadisticaVo

class LogicaEstadistica:
    def __init__(self):
        self.dao = EstadisticaDao()

    def obtener_estadisticas(self, tipo: str) -> EstadisticaVo:
        if tipo == 'Pagos':
            datos = self.dao.obtener_pagos()
        elif tipo == 'Incidencias':
            datos = self.dao.obtener_incidencias()
       
        else:
            datos = []
        return EstadisticaVo(tipo, datos)
    
    def obtener_total_pagos_por_rol(self):
        return self.dao.obtener_total_pagos_por_rol()
    
    def obtener_estadisticas_incidencias(self):
        return self.dao.obtener_total_incidencias_por_rol()
    
    def obtener_estadisticas_menus(self):
        return self.dao.obtener_total_menus_por_rol()

