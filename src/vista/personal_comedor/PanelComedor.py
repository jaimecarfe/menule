from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QInputDialog, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from src.vista.comun.ConfiguracionUsuario import ConfiguracionUsuario
from src.vista.VentanaBase import VentanaBase
from PyQt5 import uic
from src.vista.personal_comedor.ModificarMenuConAlergenos import ModificarMenuConAlergenos
from src.vista.personal_comedor.ProcesarPedidos import ProcesarPedidos
from src.vista.personal_comedor.VisualizarMenu import VisualizarMenu
from src.controlador.ControladorComedor import ControladorComedor
from src.vista.personal_comedor.StockComedor import StockComedor
from src.vista.comun.ReportarIncidenciaGeneral import ReportarIncidenciaGeneral

Form, Window = uic.loadUiType("./src/vista/ui/PanelComedor.ui")

class PanelComedor(VentanaBase, Form):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.controlador = ControladorComedor(usuario)
        self.setupUi(self)
        self.setWindowTitle("Panel - Personal Comedor")
        self.labelTitulo.setText(f"Bienvenido/a, {usuario.nombre}")

        pixmap = QPixmap("./src/vista/imagenes/paneles.png")
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.labelFoto.setPixmap(pixmap)
        self.labelFoto.setAlignment(Qt.AlignCenter)

        self.btnVerMenu.clicked.connect(self.abrir_menu)
        self.btnModificarMenu.clicked.connect(self.abrir_modificar_menu)
        self.btnConfig.clicked.connect(self.abrir_configuracion)

        self.btnProcesarPedidos.clicked.connect(self.procesar_pedidos)
        self.btnConsultarStock.clicked.connect(self.consultar_stock)

        self.btnDarseDeBaja.clicked.connect(self.dar_de_baja)
        self.btnReportarIncidencia.clicked.connect(self.reportar_incidencia)

    def abrir_menu(self):
        self.menu_window = VisualizarMenu(self.usuario, parent=self)
        self.hide()
        self.menu_window.show()

    def abrir_modificar_menu(self):
        self.mod_window = ModificarMenuConAlergenos(self.usuario)
        self.mod_window.show()

    def abrir_configuracion(self):
        self.config_window = ConfiguracionUsuario(self.usuario, self.confirmar_cerrar_sesion)
        self.config_window.show()

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
        self.login_window.controlador = ControladorPrincipal(self.login_window)
        self.login_window.show()

    def procesar_pedidos(self):
        self.ventana_pedidos = ProcesarPedidos(self.usuario)
        self.ventana_pedidos.show()

    def consultar_stock(self):
        self.ventana_stock = StockComedor()
        self.ventana_stock.show()
    
    def reportar_incidencia(self):
        self.ventana_incidencia = ReportarIncidenciaGeneral()
        self.ventana_incidencia.show()
    
    def dar_de_baja(self):
        print("Dar de baja cuenta...")
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