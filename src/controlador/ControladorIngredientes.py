from src.modelo.BussinessObject import BussinessObject

class ControladorIngredientes:
    def __init__(self):
        self._modelo = BussinessObject()

    def obtener_ingredientes(self):
        return self._modelo.ingrediente_service.obtener_ingredientes()

    def actualizar_ingrediente(self, *args):
        return self._modelo.ingrediente_service.actualizar_ingrediente(*args)

    def guardar_nuevo_ingrediente(self, *args):
        return self._modelo.ingrediente_service.guardar_nuevo_ingrediente(*args)
