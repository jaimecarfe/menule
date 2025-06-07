from src.modelo.dao.IncidenciaDao import IncidenciaDao
from src.modelo.vo.IncidenciaVo import IncidenciaVo

class LogicaIncidencia:
    def __init__(self):
        self.incidencia_dao = IncidenciaDao()

    def reportar_incidencia(self, incidencia_vo: IncidenciaVo) -> int | None:
        return self.incidencia_dao.insertar_incidencia(incidencia_vo)

    def obtener_todas(self):
        return self.incidencia_dao.obtener_todas()

    def resolver_incidencia(self, id_incidencia: int, solucion: str) -> bool:
        return self.incidencia_dao.resolver(id_incidencia, solucion)

    def actualizar_estado(self, id_incidencia: int, nuevo_estado: str) -> bool:
        return self.incidencia_dao.actualizar_estado(id_incidencia, nuevo_estado)

    def responder_incidencia(self, id_incidencia: int, respuesta: str, fecha) -> bool:
        return self.incidencia_dao.responder_incidencia(id_incidencia, respuesta, fecha)