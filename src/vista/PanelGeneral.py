from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from src.vista.administrador.ConfiguracionSistema import ConfiguracionSistema
from src.vista.estudiante.MenuEstudiante import MenuEstudiante  # puedes usar también MenuProfesor/MenuVisitante si lo prefieres
from src.controlador.ControladorAdmin import ControladorAdmin


class PanelGeneral(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"Panel General - {usuario.nombre} ({usuario.rol})")

        self.layout = QVBoxLayout()

        self.label = QLabel(f"Bienvenido, {usuario.nombre}")
        self.layout.addWidget(self.label)

        self.botonMenu = QPushButton("Ver Menú")
        self.botonMenu.clicked.connect(self.abrir_menu)
        self.layout.addWidget(self.botonMenu)

        self.botonConfig = QPushButton("Configuración")
        self.botonConfig.clicked.connect(self.abrir_configuracion)
        self.layout.addWidget(self.botonConfig)

        self.setLayout(self.layout)

        self.controlador = ControladorAdmin(self)


    def abrir_menu(self):
        self.ventana_menu = MenuEstudiante(self.usuario)  # o MenuProfesor/MenuVisitante
        self.ventana_menu.show()

    def abrir_configuracion(self):
        self.ventana_config = ConfiguracionSistema(self.controlador)
        self.ventana_config.show()

