from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from src.vista.VentanaBase import VentanaBase
from src.vista.administrador.AdminPanel import AdminPanel
from src.vista.estudiante.PanelEstudiante import PanelEstudiante
from src.vista.profesor.PanelProfesor import PanelProfesor
from src.vista.visitante.MenuVisitante import MenuVisitante
from src.vista.personal_comedor.PanelComedor import PanelComedor
from src.controlador.ControladorPrincipal import ControladorPrincipal
from src.modelo.BussinessObject import BussinessObject

Form, Window = uic.loadUiType("./src/vista/ui/VistaLogging.ui")

class Login(VentanaBase, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._modelo = BussinessObject()
        self._controlador = ControladorPrincipal(self, self._modelo)

        self.setWindowTitle("MenULE - Iniciar Sesión")
        self.resize(432, 505)
        self.showFullScreen()

        self.pushButton_aceptar.clicked.connect(self.on_button_click)
        self.label_visitante.mousePressEvent = self.abrir_vista_visitante

        try:
            self.pushButton_registro.clicked.connect(self.abrir_registro)
        except AttributeError:
            pass

    def abrir_vista_visitante(self, event):
        self.close()
        self.deleteLater()
        self.ventana_visitante = MenuVisitante()
        self.ventana_visitante.show()
        self.hide()

    def on_button_click(self):
        correo = self.lineEdit_usuario.text()
        contraseña = self.lineEdit_contrasena.text()

        if not correo or not contraseña:
            QMessageBox.warning(self, "Campos requeridos", "Completa todos los campos.")
            return

        usuario = self._controlador.login(correo, contraseña)

        if usuario:
            if usuario.rol == "administrador":
                self.ventana = AdminPanel(usuario)
                self.ventana.callback_cerrar_sesion = self.volver_al_login
            elif usuario.rol == "estudiante":
                self.ventana = PanelEstudiante(usuario)
                self.ventana.callback_cerrar_sesion = self.volver_al_login
            elif usuario.rol == "profesor":
                self.ventana = PanelProfesor(usuario)
                self.ventana.callback_cerrar_sesion = self.volver_al_login
            elif usuario.rol == "personal_comedor":
                self.ventana = PanelComedor(usuario)
                self.ventana.callback_cerrar_sesion = self.volver_al_login
            else:
                QMessageBox.warning(self, "Acceso denegado", f"Rol no autorizado: {usuario.rol}")
                return

            self.ventana.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Correo, contraseña inválidos o usuario desactivado.")

    def abrir_registro(self):
        from src.vista.Registro import Registro
        self.close()
        self.deleteLater()
        self.ventana_registro = Registro(volver_a=self)
        self.ventana_registro._controlador = self._controlador
        self.ventana_registro.show()

    def volver_al_login(self):
        self.login = Login()
        self.login.show()