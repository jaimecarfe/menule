from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.modelo.vo.UserVo import UserVo
from datetime import date

Form, Window = uic.loadUiType("src/vista/ui/VistaRegistro.ui")

class Registro(QMainWindow, Form):
    def __init__(self, volver_a=None):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        self._ventana_anterior = volver_a

        self.setWindowTitle("MenULE - Registro")
        self.pushButton_registrar.clicked.connect(self.on_registrar)
        self.pushButton_volver.clicked.connect(self.volver)
        self.comboBox_rol.currentIndexChanged.connect(self.on_rol_cambiado)
        self.on_rol_cambiado()

    def on_rol_cambiado(self):
        rol = self.comboBox_rol.currentText()
        self.lineEdit_tui.setVisible(rol == "estudiante")
        self.lineEdit_grado.setVisible(rol in ["estudiante", "profesor"])
        self.lineEdit_especialidad.setVisible(rol == "personal_comedor")

    def on_registrar(self):
        nombre = self.lineEdit_nombre.text()
        apellido = self.lineEdit_apellido.text()
        correo = self.lineEdit_correo.text()
        contrasena = self.lineEdit_password.text()
        rol = self.comboBox_rol.currentText()
        tui = self.lineEdit_tui.text() if rol == "estudiante" else None
        grado = self.lineEdit_grado.text() if rol in ["estudiante", "profesor"] else None
        especialidad = self.lineEdit_especialidad.text() if rol == "personal_comedor" else None
        dni = self.lineEdit_dni.text()
        telefono = self.lineEdit_telefono.text()
        fecha_alta = date.today()

        if not all([nombre, apellido, correo, contrasena, rol]):
            QMessageBox.warning(self, "Campos obligatorios", "Por favor, completa todos los campos obligatorios.")
            return

        user = UserVo(
            idUser=None,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contrasena,
            rol=rol,
            saldo=0.0,
            tui=tui,
            dni=dni,
            telefono=telefono,
            fecha_alta=fecha_alta,
            activo=True,
            grado_academico=grado,
            especialidad=especialidad
        )

        if self._controlador.insertar_usuario(user):
            QMessageBox.information(self, "Registro exitoso", "Usuario registrado correctamente.")
            self.close()
            if self._ventana_anterior:
                self._ventana_anterior.show()
        else:
            QMessageBox.critical(self, "Error", "El correo ya existe o hubo un error al registrar.")

    def volver(self):
        self.close()
        if self._ventana_anterior:
            self._ventana_anterior.show()

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, controlador):
        self._controlador = controlador
