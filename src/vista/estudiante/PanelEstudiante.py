from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.vista.estudiante.MenuEstudiante import MenuEstudiante
from src.vista.comun.ConfiguracionUsuario import ConfiguracionUsuario
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.vista.VentanaBase import VentanaBase


Form, Window = uic.loadUiType("./src/vista/ui/PanelEstudiante.ui")

class PanelEstudiante(VentanaBase, Form):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.controlador = ControladorEstudiante(self.usuario)

        self.setupUi(self)  # Carga el diseño desde el .ui
        self.setWindowTitle(f"MenULE - Panel de {usuario.nombre}")
        self.labelTitulo.setText(f"Bienvenido/a, {usuario.nombre}")

        # Conectar botones definidos en el .ui
        self.btnVerMenu.clicked.connect(self.abrir_menu)
        self.btnConfiguracion.clicked.connect(self.abrir_configuracion)
        self.btnHistorialReservas.clicked.connect(self.ver_historial)
        self.btnReportarIncidencia.clicked.connect(self.reportar_incidencia)

    def abrir_menu(self):
        self.menu_window = MenuEstudiante(self.usuario)
        self.menu_window.show()

    def abrir_configuracion(self):
        self.config_window = ConfiguracionUsuario(self.usuario, self.confirmar_cerrar_sesion)
        self.config_window.show()

    def ver_historial(self):
        QMessageBox.information(self, "Historial de Reservas", "Aquí se mostrará el historial.")

    def reportar_incidencia(self):
        QMessageBox.information(self, "Reportar Incidencia", "Aquí se podrá reportar una incidencia.")

    def confirmar_cerrar_sesion(self):
        respuesta = QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.cerrar_sesion()

    def cerrar_sesion(self):
        from src.vista.Login import Login
        from src.controlador.ControladorPrincipal import ControladorPrincipal

        self.close()
        self.login_window = Login()
        self.login_window.controlador = ControladorPrincipal(self.login_window, self.login_window)
        self.login_window.show()
