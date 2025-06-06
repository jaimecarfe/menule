from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QInputDialog, QDialog, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from src.vista.estudiante.MenuEstudiante import MenuEstudiante
from src.vista.comun.ConfiguracionUsuario import ConfiguracionUsuario
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.vista.VentanaBase import VentanaBase
from src.vista.comun.AgregarFondosDialog import AgregarFondosDialog
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.Sesion import Sesion
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.controlador.ControladorProfesor import ControladorProfesor
from src.controlador.ControladorComedor import ControladorComedor
import uuid
from src.vista.comun.ReportarIncidenciaGeneral import ReportarIncidenciaGeneral

Form, Window = uic.loadUiType("./src/vista/ui/PanelEstudiante.ui")

class PanelEstudiante(VentanaBase, Form):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.controlador = ControladorEstudiante()
        self.setupUi(self)
        self.setWindowTitle(f"MenULE - Panel de {usuario.nombre}")
        self.labelTitulo.setText(f"Bienvenido/a, {usuario.nombre}")
        self.btn_add_fondos.clicked.connect(self.agregar_fondos)


        saldo_real = self.controlador.obtener_saldo(self.usuario.idUser)
        self.usuario.saldo = saldo_real
        self.saldo_label.setText(f"Saldo: {saldo_real:.2f}€")

        pixmap = QPixmap("./src/vista/imagenes/paneles.png")
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.labelFoto.setPixmap(pixmap)
        self.labelFoto.setAlignment(Qt.AlignCenter)
        
        self.btnVerMenu.clicked.connect(self.abrir_menu)
        self.btnConfiguracion.clicked.connect(self.abrir_configuracion)
        self.btnHistorialReservas.clicked.connect(self.ver_historial)
        self.btnReportarIncidencia.clicked.connect(self.abrir_ventana_incidencia)
        self.btnDarseDeBaja.clicked.connect(self.dar_de_baja)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.actualizar_saldo_ui()
    
    def abrir_menu(self):
        self.menu_window = MenuEstudiante(self.usuario, parent=self)
        self.hide()  # Oculta el panel actual
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

    def dar_de_baja(self):
        respuesta = QMessageBox.question(
            self,
            "Dar de Baja",
            "¿Estás seguro de que deseas dar de baja tu cuenta?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.controlador.dar_de_baja()
            QMessageBox.information(self, "Cuenta", "Tu cuenta ha sido dada de baja.")
            self.cerrar_sesion()

    def cerrar_sesion(self):
        from src.vista.Login import Login
        from src.controlador.ControladorPrincipal import ControladorPrincipal

        self.close()
        self.login_window = Login()
        self.login_window.controlador = ControladorPrincipal(self.login_window)
        self.login_window.show()
        
    def actualizar_saldo_ui(self):
        saldo_actualizado = self.controlador.obtener_saldo(self.usuario.idUser)
        self.usuario.saldo = saldo_actualizado
        self.saldo_label.setText(f"Saldo: {saldo_actualizado:.2f}€")

    def agregar_fondos(self):
        dialog = AgregarFondosDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            cantidad = dialog.cantidad
            nuevo_saldo = self.usuario.saldo + cantidad
            if self.controlador.actualizar_saldo(self.usuario.idUser, nuevo_saldo):
                self.actualizar_saldo_ui()
                QMessageBox.information(self, "Éxito", "Fondos añadidos correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el saldo.")

    def abrir_ventana_incidencia(self):
        self.ventana_incidencia = ReportarIncidenciaGeneral()
        self.ventana_incidencia.show()
