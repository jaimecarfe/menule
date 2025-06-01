from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from src.vista.estudiante.MenuEstudiante import MenuEstudiante
from src.vista.personal_comedor.ModificarMenu import ModificarMenu
#from src.vista.comun.TablaAlergenos import TablaAlergenos
from src.vista.comun.ConfiguracionUsuario import ConfiguracionUsuario
#from src.vista.comun.VerIncidencias import VerIncidencias

class PanelComedor(QWidget):
    def __init__(self, usuario, callback_cerrar_sesion=None):
        super().__init__()
        self.usuario = usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion

        self.setWindowTitle("Panel - Personal Comedor")
        self.setGeometry(200, 100, 400, 400)

        layout = QVBoxLayout()

        # Ver Menú
        btn_ver_menu = QPushButton("Ver Menú")
        btn_ver_menu.clicked.connect(self.abrir_menu)
        layout.addWidget(btn_ver_menu)

        # Modificar Menú
        btn_modificar_menu = QPushButton("Modificar Menú")
        btn_modificar_menu.clicked.connect(self.abrir_modificar_menu)
        layout.addWidget(btn_modificar_menu)

        '''
        # Ver Incidencias
        btn_ver_incidencias = QPushButton("Ver Incidencias")
        btn_ver_incidencias.clicked.connect(self.abrir_incidencias)
        layout.addWidget(btn_ver_incidencias)

        # Tabla de Alérgenos
        btn_alergenos = QPushButton("Tabla de Alérgenos")
        btn_alergenos.clicked.connect(self.abrir_alergenos)
        layout.addWidget(btn_alergenos)
        '''

        # Configuración
        btn_config = QPushButton("Configuración")
        btn_config.clicked.connect(self.abrir_configuracion)
        layout.addWidget(btn_config)

        self.setLayout(layout)

    def abrir_menu(self):
        self.menu_window = MenuEstudiante(self.usuario)
        self.menu_window.show()

    def abrir_modificar_menu(self):
        self.mod_window = ModificarMenu()
        self.mod_window.show()
    '''
    def abrir_incidencias(self):
        self.inc_window = VerIncidencias(self.usuario)
        self.inc_window.show()

    def abrir_alergenos(self):
        self.alerg_window = TablaAlergenos()
        self.alerg_window.show()
    '''
    def abrir_configuracion(self):
        self.config_window = ConfiguracionUsuario(self.usuario, callback_cerrar_sesion=self.cerrar_sesion)
        self.config_window.show()

    def cerrar_sesion(self):
        self.close()
        if self.callback_cerrar_sesion:
            self.callback_cerrar_sesion()
