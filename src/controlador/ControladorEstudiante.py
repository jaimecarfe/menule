from src.modelo.BussinessObject import BussinessObject
from src.modelo.Sesion import Sesion

"""
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.vo.MenuVo import MenuVo
from src.modelo.vo.UserVo import UserVo
"""
class ControladorEstudiante:
    def __init__(self):
        self._modelo = BussinessObject()

    def hacer_reserva(self, id_menu, fecha):
        usuario = Sesion().get_usuario()  # <-- Obtén el usuario logueado
        # Aquí puedes usar usuario.idUser, usuario.nombre, etc.
        pass

    def cancelar_reserva(self, id_reserva, motivo):
        usuario = Sesion().get_usuario()
        pass

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