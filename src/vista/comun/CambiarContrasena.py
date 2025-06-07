from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
from src.modelo.Sesion import Sesion
from src.controlador.ControladorUsuarios import ControladorUsuarios

class CambiarContrasena(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cambiar Contraseña")
        self.setGeometry(400, 400, 300, 200)

        self.controlador = ControladorUsuarios()

        layout = QVBoxLayout()

        self.input_actual = QLineEdit()
        self.input_actual.setEchoMode(QLineEdit.Password)
        self.input_actual.setPlaceholderText("Contraseña actual")

        self.input_nueva = QLineEdit()
        self.input_nueva.setEchoMode(QLineEdit.Password)
        self.input_nueva.setPlaceholderText("Nueva contraseña")

        self.input_repetir = QLineEdit()
        self.input_repetir.setEchoMode(QLineEdit.Password)
        self.input_repetir.setPlaceholderText("Repetir nueva contraseña")

        self.btn_cambiar = QPushButton("Cambiar")
        self.btn_cambiar.clicked.connect(self.cambiar)

        layout.addWidget(QLabel("Introduce tus credenciales:"))
        layout.addWidget(self.input_actual)
        layout.addWidget(self.input_nueva)
        layout.addWidget(self.input_repetir)
        layout.addWidget(self.btn_cambiar)

        self.setLayout(layout)

    def cambiar(self):
        actual = self.input_actual.text()
        nueva = self.input_nueva.text()
        repetir = self.input_repetir.text()
        usuario = Sesion().get_usuario()

        ok, mensaje = self.controlador.cambiar_contrasena(usuario, actual, nueva, repetir)

        if ok:
            QMessageBox.information(self, "Éxito", mensaje)
            self.close()
        else:
            QMessageBox.warning(self, "Error", mensaje)
