from src.modelo.BussinessObject import BussinessObject

class ControladorIncidencias:
    def __init__(self):
        self._modelo = BussinessObject()

    def reportar_incidencia(self, incidencia_vo):
        return self._modelo.incidencia_service.reportar_incidencia(incidencia_vo)
    
    def obtener_todas(self):
        return self._modelo.incidencia_service.obtener_todas()

    def cambiar_estado(self, id_incidencia, nuevo_estado):
        return self._modelo.incidencia_service.actualizar_estado(id_incidencia, nuevo_estado)

    def responder_incidencia(self, id_incidencia, respuesta, fecha):
        return self._modelo.incidencia_service.responder_incidencia(id_incidencia, respuesta, fecha)