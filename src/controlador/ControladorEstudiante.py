from src.modelo.Sesion import Sesion
from src.controlador.ControladorReservas import ControladorReservas
from src.controlador.ControladorIncidencias import ControladorIncidencias
from src.modelo.BussinessObject import BussinessObject

class ControladorEstudiante:
    def __init__(self):
        self._modelo = BussinessObject()
        self.reserva_ctrl = ControladorReservas()
        self.incidencia_ctrl = ControladorIncidencias()

    def obtener_menus_disponibles(self):
        return self._modelo.menu_service.obtener_menus_disponibles()

    def hacer_reserva(self, id_usuario: int, fecha: str):
        return self.reserva_ctrl.hacer_reserva(id_usuario, fecha)

    def hacer_reserva_completa(self, id_usuario, fecha, primero, segundo, postre):
        return self.reserva_ctrl.hacer_reserva_completa(id_usuario, fecha, primero, segundo, postre)

    def crear_reserva(self, reserva_vo):
        return self.reserva_ctrl.crear_reserva(reserva_vo)

    def obtener_ultima_reserva_id(self, id_usuario):
        return self.reserva_ctrl.obtener_ultima_reserva_id(id_usuario)

    def obtener_reservas_estudiante(self, id_usuario):
        return self.reserva_ctrl.obtener_reservas_estudiante(id_usuario)

    def obtener_platos_por_fecha(self, fecha):
        return self._modelo.menu_service.obtener_menu_por_fecha(fecha)

    def reportar_incidencia(self, incidencia_vo):
        self.incidencia_ctrl.reportar_incidencia(incidencia_vo)

    def obtener_saldo(self, id_usuario):
        return self._modelo.usuario_service.obtener_saldo(id_usuario)

    def actualizar_saldo(self, id_usuario, nuevo_saldo):
        return self._modelo.usuario_service.actualizar_saldo(id_usuario, nuevo_saldo)

    def dar_de_baja(self):
        usuario = Sesion().get_usuario()
        self._modelo.usuario_service.dar_de_baja_y_cerrar_sesion(usuario.idUser)

    def reservar_menu(self, id_usuario, fecha, primero, segundo, postre):
        return self._modelo.reserva_service.crear_reserva_completa(id_usuario, fecha, primero, segundo, postre)