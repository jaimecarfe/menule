from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import bcrypt
from src.modelo.dao.UserDao import UserDao

class CambiarContrasena(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.user_dao = UserDao()

        self.setWindowTitle("Cambiar contraseña")
        self.setGeometry(300, 300, 350, 200)

        layout = QVBoxLayout()

        self.input_actual = QLineEdit()
        self.input_actual.setEchoMode(QLineEdit.Password)
        self.input_actual.setPlaceholderText("Contraseña actual")
        layout.addWidget(QLabel("Contraseña actual"))
        layout.addWidget(self.input_actual)

        self.input_nueva = QLineEdit()
        self.input_nueva.setEchoMode(QLineEdit.Password)
        self.input_nueva.setPlaceholderText("Nueva contraseña")
        layout.addWidget(QLabel("Nueva contraseña"))
        layout.addWidget(self.input_nueva)

        self.input_repetida = QLineEdit()
        self.input_repetida.setEchoMode(QLineEdit.Password)
        self.input_repetida.setPlaceholderText("Repetir nueva contraseña")
        layout.addWidget(QLabel("Repetir nueva contraseña"))
        layout.addWidget(self.input_repetida)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.cambiar_contrasena)
        layout.addWidget(self.boton_guardar)

        self.setLayout(layout)

    def cambiar_contrasena(self):
        actual = self.input_actual.text()
        nueva = self.input_nueva.text()
        repetida = self.input_repetida.text()

        if not bcrypt.checkpw(actual.encode(), self.usuario.contrasena.encode()):
            QMessageBox.critical(self, "Error", "La contraseña actual es incorrecta.")
            return

        if nueva != repetida:
            QMessageBox.warning(self, "Error", "Las nuevas contraseñas no coinciden.")
            return

        nueva_hash = bcrypt.hashpw(nueva.encode(), bcrypt.gensalt()).decode()
        self.usuario.contrasena = nueva_hash
        actualizado = self.user_dao.actualizar_contrasena(self.usuario.idUser, nueva_hash)

        if actualizado:
            QMessageBox.information(self, "Éxito", "Contraseña actualizada correctamente.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar la contraseña.")
