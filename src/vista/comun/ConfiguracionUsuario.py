from src.vista.comun.CambiarContrasena import CambiarContrasena
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QApplication

class ConfiguracionUsuario(QWidget):
    def __init__(self, usuario, callback_cerrar_sesion=None):
        super().__init__()
        self.usuario = usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion

        self.setWindowTitle("Configuración de cuenta")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.btn_cambiar_contrasena = QPushButton("Cambiar contraseña")
        self.btn_cambiar_contrasena.clicked.connect(self.cambiar_contrasena)
        layout.addWidget(self.btn_cambiar_contrasena)

        self.btn_cerrar_sesion = QPushButton("Cerrar sesión")
        self.btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btn_cerrar_sesion)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
            background-color: #e6f2ff;
            font-family: Arial;
            font-size: 14px;
        }
        QLabel {
            color: #005c99;
            font-weight: bold;
        }
        QLineEdit {
            border: 1px solid #80bfff;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QPushButton {
            background-color: #00cc99;
            color: white;
            border-radius: 10px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #009973;
        }
        """)

    def cambiar_contrasena(self):
        self.ventana_cambio = CambiarContrasena(self.usuario)
        self.ventana_cambio.show()

    def cerrar_sesion(self):
        if self.callback_cerrar_sesion:
            self.callback_cerrar_sesion()
        self.close()
