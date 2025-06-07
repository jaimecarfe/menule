from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
from src.modelo.Sesion import Sesion
from src.controlador.ControladorUsuarios import ControladorUsuarios

class CambiarContrasena(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cambiar Contraseña")
        self.setMinimumSize(380, 320)

        self.controlador = ControladorUsuarios()

        self.setStyleSheet("""
QWidget {
    background-color: #e6f2ff;
    font-family: Arial, sans-serif;
    font-size: 16px;
    color: #1a1a1a;
}
QLabel {
    color: #0080b2;
    font-weight: bold;
    font-size: 17px;
    margin-bottom: 2px;
}
QLineEdit {
    border: 1.5px solid #80bfff;
    border-radius: 8px;
    padding: 10px 8px;
    background-color: #f7fbff;
    color: #000000;
    font-size: 16px;
    margin-bottom: 10px;
}
QPushButton {
    background-color: #00cc99;
    color: white;
    border-radius: 14px;
    padding: 12px 0;
    font-size: 16px;
    margin-top: 14px;
    margin-bottom: 8px;
}
QPushButton:hover {
    background-color: #009973;
}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 18, 28, 18)
        layout.setSpacing(6)

        label = QLabel("Cambia tu contraseña")
        label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(label)

        layout.addSpacing(4)

        self.input_actual = QLineEdit()
        self.input_actual.setEchoMode(QLineEdit.Password)
        self.input_actual.setPlaceholderText("Contraseña actual")

        self.input_nueva = QLineEdit()
        self.input_nueva.setEchoMode(QLineEdit.Password)
        self.input_nueva.setPlaceholderText("Nueva contraseña")

        self.input_repetir = QLineEdit()
        self.input_repetir.setEchoMode(QLineEdit.Password)
        self.input_repetir.setPlaceholderText("Repetir nueva contraseña")

        layout.addWidget(self.input_actual)
        layout.addWidget(self.input_nueva)
        layout.addWidget(self.input_repetir)

        self.btn_cambiar = QPushButton("Cambiar contraseña")
        self.btn_cambiar.clicked.connect(self.cambiar)
        layout.addWidget(self.btn_cambiar)

        # Espaciador para centrar verticalmente si la ventana se agranda
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

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