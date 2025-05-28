from PyQt5.QtWidgets import QMessageBox
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorAdmin import ControladorAdmin
from PyQt5 import uic
from src.vista.administrador.Estadisticas import VentanaEstadisticas

Form, Window = uic.loadUiType("./src/vista/ui/AdminPanel.ui")

class AdminPanel(VentanaBase, Form):
    def __init__(self, usuario):
        super().__init__()
        self.setupUi(self)
        self.usuario = usuario
        self._controlador = ControladorAdmin(self)
        self._callback_cerrar_sesion = None
        self.btnCerrarSesion.clicked.connect(self.confirmar_cerrar_sesion)

        # --- Integración de la pestaña de estadísticas ---
        # Si ya tienes un tab de estadísticas en el UI, reemplaza el widget por VentanaEstadisticas
        # Si no lo tienes, añade uno nuevo
        self.tabEstadisticas = VentanaEstadisticas(self)
        self.tabPanel.addTab(self.tabEstadisticas, "Estadísticas")    

    @property
    def callback_cerrar_sesion(self):
        return self._callback_cerrar_sesion

    @callback_cerrar_sesion.setter
    def callback_cerrar_sesion(self, callback):
        self._callback_cerrar_sesion = callback

    def confirmar_cerrar_sesion(self):
        respuesta = QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes and self._callback_cerrar_sesion:
            self.close()
            self._callback_cerrar_sesion()