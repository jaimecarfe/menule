from src.modelo.BussinessObject import BussinessObject

class ControladorConfiguracion:
    def __init__(self):
        self._modelo = BussinessObject()

    def obtener_configuraciones(self):
        return self._modelo.configuracion_service.obtener_configuraciones()

    def guardar_configuracion(self, clave, valor):
        return self._modelo.configuracion_service.guardar_configuracion(clave, valor)
