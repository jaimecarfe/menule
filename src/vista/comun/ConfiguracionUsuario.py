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
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #e0e0e0, stop:1 #f5f5f5);
            }
            QPushButton {
            background-color: #bdbdbd;
            color: black;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px;
            }
            QPushButton:hover {
            background-color: #9e9e9e;
            }
        """)

    def cambiar_contrasena(self):
        self.ventana_cambio = CambiarContrasena(self.usuario)
        self.ventana_cambio.show()

    def cerrar_sesion(self):
        if self.callback_cerrar_sesion:
            self.callback_cerrar_sesion()
        self.close()
