from src.controlador.ControladorReservas import ControladorReservas
from src.controlador.ControladorIncidencias import ControladorIncidencias
from src.controlador.ControladorTickets import ControladorTickets
from src.modelo.BussinessObject import BussinessObject
from src.controlador.ControladorUsuarios import ControladorUsuarios
from src.modelo.Sesion import Sesion

class ControladorComedor:
    def __init__(self, usuario_actual):
        self._usuario = usuario_actual
        self._modelo = BussinessObject()
        self.reserva_ctrl = ControladorReservas()
        self.incidencia_ctrl = ControladorIncidencias()
        self.ticket_ctrl = ControladorTickets()
        self.usuario_ctrl = ControladorUsuarios()
        # self.ingrediente_ctrl = ControladorIngredientes()

    def procesar_ticket(self, codigo_qr):
        return self.ticket_ctrl.validar_ticket(codigo_qr)

    def consultar_reservas_por_plato(self, id_menu):
        pass

    def ver_stock(self):
        pass

    def obtener_reservas(self):
        return self.reserva_ctrl.obtener_todas_las_reservas()

    def reportar_incidencia(self, incidencia_vo):
        return self.incidencia_ctrl.reportar_incidencia(incidencia_vo)

    def guardar_menu_con_alergenos(self, fecha: str, lista_platos: list[tuple]) -> bool:
        return self._modelo.menu_service.guardar_menu_con_alergenos(fecha, lista_platos)

    def obtener_reservas_confirmadas(self):
        return self._modelo.reserva_service.obtener_reservas_confirmadas()

    def obtener_platos_por_fecha(self, fecha):
        return self._modelo.menu_service.obtener_menu_por_fecha(fecha)

    def dar_de_baja(self):
        usuario = Sesion().get_usuario()
        self._modelo.usuario_service.dar_de_baja_usuario(usuario.idUser)
        Sesion().cerrar_sesion()