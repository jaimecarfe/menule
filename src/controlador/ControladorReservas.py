from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.ReservaVo import ReservaVo

class ControladorReservas:
    def __init__(self):
        self._modelo = BussinessObject()

    def hacer_reserva(self, id_usuario, fecha):
        return self._modelo.reserva_service.crear_reserva_por_fecha(id_usuario, fecha)

    def hacer_reserva_completa(self, id_usuario, fecha, primero, segundo, postre):
        return self._modelo.reserva_service.crear_reserva_completa(id_usuario, fecha, primero, segundo, postre)

    def crear_reserva(self, reserva_vo: ReservaVo):
        return self._modelo.reserva_service.crear_reserva(reserva_vo)

    def obtener_ultima_reserva_id(self, id_usuario):
        return self._modelo.reserva_service.obtener_ultima_reserva_id(id_usuario)

    def obtener_reservas_estudiante(self, id_usuario):
        return self._modelo.reserva_service.obtener_reservas_estudiante(id_usuario)

    def obtener_todas_las_reservas(self):
        return self._modelo.reserva_service.listar_reservas()
    
    def obtener_reservas_con_detalle(self, estados=('confirmada', 'pendiente')):
        return self._modelo.reserva_service.obtener_reservas_con_detalle(estados)

    def actualizar_estado_reserva(self, id_reserva, bit):
        return self._modelo.reserva_service.actualizar_estado_reserva(id_reserva, bit)
