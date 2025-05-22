from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.modelo.vo.UserVo import UserVo

Form, Window = uic.loadUiType("./src/vista/ui/VistaRegistro.ui")

class Registro(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None

        self.setWindowTitle("MenULE - Registro")
        self.resize(432, 505)

        self.pushButton_registrar.clicked.connect(self.on_button_click)

    def on_button_click(self):
        nombre = self.lineEdit_nombre.text()
        apellido = self.lineEdit_apellido.text()
        correo = self.lineEdit_email.text()
        contraseña = self.lineEdit_password.text()
        rol = self.comboBox_rol.currentText()
        tui = self.lineEdit_tui.text() if rol == "estudiante" else None

        if not all([nombre, apellido, correo, contraseña, rol]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        nuevo_usuario = UserVo(
            idUser=None,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contraseña,
            rol=rol,
            saldo=0.0,
            tui=tui
        )

        if self._controlador.insertar_usuario(nuevo_usuario):
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "El correo ya está registrado.")

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, controlador):
        self._controlador = controlador
