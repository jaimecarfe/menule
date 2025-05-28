from PyQt5.QtWidgets import QMessageBox
from src.vista.VentanaBase import VentanaBase
from PyQt5 import uic
from src.vista.administrador.AdminPanel import AdminPanel
from src.vista.PanelGeneral import PanelGeneral  # el nuevo que creamos


Form, Window = uic.loadUiType("./src/vista/ui/VistaLogging.ui")

class Login(VentanaBase, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None

        self.setWindowTitle("MenULE - Iniciar Sesión")
        self.resize(432, 505)

        self.pushButton_aceptar.clicked.connect(self.on_button_click)

        # Conectar botón de registro si está definido
        try:
            self.pushButton_registro.clicked.connect(self.abrir_registro)
        except AttributeError:
            pass

    def on_button_click(self):
        correo = self.lineEdit_usuario.text()
        contraseña = self.lineEdit_contrasena.text()

        if not correo or not contraseña:
            QMessageBox.warning(self, "Campos requeridos", "Completa todos los campos.")
            return

        if not self._controlador:
            QMessageBox.critical(self, "Error interno", "Controlador no definido.")
            return

        usuario = self._controlador.login_usuario(correo, contraseña)

        if usuario:

            if usuario.rol == "administrador":
                self.ventana = AdminPanel(usuario)
            else:
                self.ventana = PanelGeneral(usuario)

            self.ventana.show()
            self.close()

        else:
            QMessageBox.critical(self, "Error", "Correo, contraseña inválidos o usuario desactivado.")

    def abrir_registro(self):
        if hasattr(self, "abrir_registro"):
            self.abrir_registro()

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, controlador):
        self._controlador = controlador