from src.modelo.dao.ConfiguracionDao import ConfiguracionDao

class LogicaConfiguracion:
    def __init__(self):
        self.dao = ConfiguracionDao()

    def obtener_configuraciones(self):
        return self.dao.obtener_configuraciones()

    def guardar_configuracion(self, clave: str, valor: str) -> bool:
        return self.dao.guardar_configuracion(clave, valor)
