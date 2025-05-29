from src.modelo.BussinessObject import BussinessObject
"""
from src.modelo.vo.ReservaVo import ReservaVo
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.vo.MenuVo import MenuVo
from src.modelo.vo.UserVo import UseroVo
"""
class ControladorEstudiante:
    def __init__(self, usuario_actual):
        self._usuario = usuario_actual
        self._modelo = BussinessObject()

    def hacer_reserva(self, id_menu, fecha):
        pass

    def cancelar_reserva(self, id_reserva, motivo):
        pass

    def ver_historial(self):
        historial = self.controlador.ver_historial_reservas()
        # Mostrar el historial como tú quieras (por ahora solo placeholder):
        QMessageBox.information(self, "Historial", "Aquí se mostrará el historial.")

    def reportar_incidencia(self):
        # Aquí podrías abrir un formulario para recoger título y descripción
        titulo = "Incidencia ejemplo"
        descripcion = "Ejemplo de reporte de incidencia."
        self.controlador.reportar_incidencia(titulo, descripcion)
        QMessageBox.information(self, "Incidencia", "¡Incidencia reportada!")
