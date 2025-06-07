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
        elif tipo == 'Menús':
            datos = self.dao.obtener_menus()
        elif tipo == 'Reservas':
            datos = self.dao.obtener_reservas()
        else:
            datos = []
        return EstadisticaVo(tipo, datos)
