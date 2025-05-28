from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from src.vista.comun.CambiarContrasena import CambiarContrasena

class ConfiguracionUsuario(QWidget):
    def __init__(self, usuario, callback_cerrar_sesion=None):
        super().__init__()
        self.usuario = usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion

        self.setWindowTitle("Configuración de cuenta")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.btn_cambiar_contrasena = QPushButton("Cambiar contraseña")
        self.btn_cambiar_contrasena.clicked.connect(self.cambiar_contrasena)
        layout.addWidget(self.btn_cambiar_contrasena)

        self.btn_restaurar = QPushButton("Restaurar configuración")
        self.btn_restaurar.clicked.connect(self.restaurar_configuracion)
        layout.addWidget(self.btn_restaurar)

        self.btn_cerrar_sesion = QPushButton("Cerrar sesión")
        self.btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btn_cerrar_sesion)

        self.setLayout(layout)

    def cambiar_contrasena(self):
        self.ventana_cambio = CambiarContrasena(self.usuario)
        self.ventana_cambio.show()


    def restaurar_configuracion(self):
        QMessageBox.information(self, "Restaurar configuración", "Configuración restaurada por defecto.")

    def cerrar_sesion(self):
        if self.callback_cerrar_sesion:
            self.callback_cerrar_sesion()
        self.close()

