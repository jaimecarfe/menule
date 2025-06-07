from src.controlador.ControladorReservas import ControladorReservas
from src.controlador.ControladorIncidencias import ControladorIncidencias
from src.modelo.BussinessObject import BussinessObject
from src.modelo.Sesion import Sesion
from PyQt5.QtWidgets import QMessageBox

class ControladorProfesor:
    def __init__(self):
        self.reserva_ctrl = ControladorReservas()
        self.incidencia_ctrl = ControladorIncidencias()
        self._modelo = BussinessObject()

    def hacer_reserva(self, id_menu, fecha):
        usuario = Sesion().get_usuario()
        # Si necesitas construir ReservaVo aquí, debes importar y hacerlo:
        # from src.modelo.vo.ReservaVo import ReservaVo
        # reserva = ReservaVo(...)
        # return self.reserva_ctrl.crear_reserva(reserva)
        pass  # completar si usas id_menu directamente

    def cancelar_reserva(self, id_reserva, motivo):
        # Esto debería implementarse en LogicaReserva y ControladorReservas
        pass

    def ver_historial(self):
        usuario = Sesion().get_usuario()
        historial = self.reserva_ctrl.obtener_reservas_estudiante(usuario.idUser)
        QMessageBox.information(None, "Historial", f"Reservas encontradas: {len(historial)}")

    def reportar_incidencia(self, incidencia_vo):
        self.incidencia_ctrl.reportar_incidencia(incidencia_vo)
        QMessageBox.information(None, "Incidencia", "¡Incidencia reportada!")

    def dar_de_baja(self):
        usuario = Sesion().get_usuario()
        self._modelo.usuario_service.dar_de_baja_usuario(usuario.idUser)
        Sesion().cerrar_sesion()

    def obtener_saldo(self, id_usuario):
        return self._modelo.usuario_service.obtener_saldo(id_usuario)

    def actualizar_saldo(self, id_usuario, nuevo_saldo):
        return self._modelo.usuario_service.actualizar_saldo(id_usuario, nuevo_saldo)
    
    def obtener_menu_por_fecha(self, fecha: str):
        return self._modelo.menu_service.obtener_menu_por_fecha(fecha)