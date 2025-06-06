from src.modelo.BussinessObject import BussinessObject
from src.modelo.Sesion import Sesion
from src.modelo.vo.ReservaVo import ReservaVo
from PyQt5.QtWidgets import QMessageBox

"""
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.vo.UserVo import UserVo
"""
class ControladorEstudiante:
    def __init__(self):
        self._modelo = BussinessObject()

    def obtener_menus_disponibles(self):
        return self._modelo.obtenerMenusDisponibles()
    
    def obtener_ultima_reserva_id(self, id_usuario):
        return self._modelo.obtenerUltimaReservaId(id_usuario)

    def hacer_reserva(self, id_usuario: int, fecha: str):
        from src.modelo.dao.MenuDao import MenuDao
        menu_dao = MenuDao()
        id_menu = menu_dao.obtener_id_menu_por_fecha(fecha)

        if not id_menu:
            print("No hay menú disponible para la fecha:", fecha)
            return None

        reserva = ReservaVo(
            id_reserva=None,
            id_usuario=id_usuario,
            id_menu=id_menu,
            fecha_reserva=None,  # Se pone en BBDD
            estado="confirmada"
        )
        id_reserva = self._modelo.crearReserva(reserva)
        return id_reserva  # <-- Devuelve el id_reserva directamente
    
    def ver_historial(self):
        usuario = Sesion().get_usuario()
        historial = self._modelo.ver_historial_reservas(usuario.idUser)  # Ejemplo de uso
        # Mostrar el historial como tú quieras (por ahora solo placeholder):
        QMessageBox.information(None, "Historial", "Aquí se mostrará el historial.")

    def reportar_incidencia(self):
        usuario = Sesion().get_usuario()
        # Aquí podrías abrir un formulario para recoger título y descripción
        titulo = "Incidencia ejemplo"
        descripcion = "Ejemplo de reporte de incidencia."
        self._modelo.reportar_incidencia(usuario.idUser, titulo, descripcion)
        QMessageBox.information(None, "Incidencia", "¡Incidencia reportada!")
    
    def dar_de_baja(self):
        usuario = Sesion().get_usuario()
        self._modelo.darDeBajaUsuario(usuario.idUser)
        Sesion().cerrar_sesion()
    
    def obtener_saldo(self, id_usuario):
        return self._modelo.obtener_saldo(id_usuario)

    def actualizar_saldo(self, id_usuario, nuevo_saldo):
        return self._modelo.actualizarSaldo(id_usuario, nuevo_saldo)

    def hacer_reserva_completa(self, id_usuario, fecha, primero, segundo, postre):
        return self._modelo.crearReservaCompleta(id_usuario, fecha, primero, segundo, postre)
    

    def crear_reserva(self, reserva_vo):
        self._modelo.insertar_reserva(reserva_vo)

    def obtener_platos_por_fecha(self, fecha):
        return self._modelo.obtenerMenuPorFecha(fecha)

