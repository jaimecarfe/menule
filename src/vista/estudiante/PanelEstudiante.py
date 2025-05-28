from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from src.vista.administrador.ConfiguracionSistema import ConfiguracionSistema
from src.vista.estudiante.MenuEstudiante import MenuEstudiante
from src.controlador.ControladorAdmin import ControladorAdmin
from src.vista.administrador.AdminPanel import AdminPanel
from src.vista.comun.ConfiguracionUsuario import ConfiguracionUsuario


class PanelEstudiante(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"MenULE - Panel de {usuario.nombre}")
        self.setGeometry(100, 100, 400, 200)

        self.controlador = ControladorAdmin()

        layout = QVBoxLayout()

        self.boton_menu = QPushButton("Ver Menú")
        self.boton_menu.clicked.connect(self.abrir_menu)
        layout.addWidget(self.boton_menu)

        self.boton_config = QPushButton("Configuración")
        self.boton_config.clicked.connect(self.abrir_configuracion)
        layout.addWidget(self.boton_config)

        self.setLayout(layout)

    def abrir_menu(self):
        self.menu_window = MenuEstudiante(self.usuario)
        self.menu_window.show()

    def abrir_configuracion(self):
        self.config_window = ConfiguracionUsuario(self.usuario, self.cerrar_sesion)
        self.config_window.show()

    def cerrar_sesion(self):
        from src.vista.Login import Login  # <--- se importa solo cuando se necesita
        from src.controlador.ControladorPrincipal import ControladorPrincipal

        self.close()
        self.login_window = Login()
        self.login_window.controlador = ControladorPrincipal(self.login_window, self.login_window)
        self.login_window.show()



