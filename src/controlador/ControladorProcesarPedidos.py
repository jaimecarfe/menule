from src.controlador.ControladorReservas import ControladorReservas

class ControladorProcesarPedidos:
    def __init__(self):
        self._ctrl_reservas = ControladorReservas()

    def obtener_reservas(self):
        return self._ctrl_reservas.obtener_reservas_con_detalle()

    def actualizar_estado(self, id_reserva, bit):
        return self._ctrl_reservas.actualizar_estado_reserva(id_reserva, bit)