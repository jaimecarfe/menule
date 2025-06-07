from src.modelo.BussinessObject import BussinessObject

class ControladorVisitante:
    def __init__(self):
        self._modelo = BussinessObject()

    def hacer_reserva_anonima(self, fecha, primero, segundo, postre):
        return self._modelo.reserva_service.crear_reserva_anonima(fecha, primero, segundo, postre)

    def obtener_menu_por_fecha(self, fecha):
        return self._modelo.menu_service.obtener_menu_por_fecha(fecha)
