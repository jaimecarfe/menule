from PyQt5.QtWidgets import QWidget
from src.vista.estudiante.MenuEstudiante import MenuEstudiante
from src.vista.personal_comedor.ModificarMenu import ModificarMenu
from src.vista.comun.ConfiguracionUsuario import ConfiguracionUsuario
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.vista.VentanaBase import VentanaBase
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/PanelComedor.ui")

class PanelComedor(VentanaBase, Form):
    def __init__(self, usuario, callback_cerrar_sesion=None):
        super().__init__()
        self.usuario = usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion

        self.setupUi(self)
        self.setWindowTitle("Panel - Personal Comedor")

        # Conectar botones a sus respectivas funciones
        self.btnVerMenu.clicked.connect(self.abrir_menu)
        self.btnModificarMenu.clicked.connect(self.abrir_modificar_menu)
        self.btnConfig.clicked.connect(self.abrir_configuracion)

        self.btnProcesarPedidos.clicked.connect(self.procesar_pedidos)
        self.btnConsultarStock.clicked.connect(self.consultar_stock)


    def abrir_menu(self):
        self.menu_window = MenuEstudiante(self.usuario)
        self.menu_window.show()

    def abrir_modificar_menu(self):
        self.mod_window = ModificarMenu()
        self.mod_window.show()

    def abrir_configuracion(self):
        self.config_window = ConfiguracionUsuario(self.usuario, callback_cerrar_sesion=self.cerrar_sesion)
        self.config_window.show()

    def cerrar_sesion(self):
        self.close()
        if self.callback_cerrar_sesion:
            self.callback_cerrar_sesion()

    def procesar_pedidos(self):
        # Lógica para procesar pedidos
        print("Procesando pedidos...")

    def consultar_stock(self):
        # Lógica para consultar stock interno
        print("Consultando stock interno...")