from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.modelo.vo.UserVo import UserVo
from src.modelo.BussinessObject import BussinessObject

Form, Window = uic.loadUiType("./src/vista/ui/RegistrarAdmin.ui")

class VentanaRegistrarAdmin(QMainWindow, Form):
    def __init__(self, callback_volver=None):
        super().__init__()
        self.setupUi(self)
        self.callback_volver = callback_volver

        self.pushButton_registrar.clicked.connect(self.registrar_usuario)
        self.pushButton_volver.clicked.connect(self.volver)

        # Conectar el cambio de rol
        self.comboBox_rol.currentTextChanged.connect(self.actualizar_campos_por_rol)
        self.actualizar_campos_por_rol(self.comboBox_rol.currentText())

    def volver(self):
        self.close()
        if self.callback_volver:
            self.callback_volver()

    def actualizar_campos_por_rol(self, rol):
        self.lineEdit_tui.setVisible(rol == "estudiante")
        self.lineEdit_grado.setVisible(rol == "profesor")
        self.lineEdit_especialidad.setVisible(rol == "personal_comedor")

    def registrar_usuario(self):
        nombre = self.lineEdit_nombre.text().strip()
        apellido = self.lineEdit_apellido.text().strip()
        correo = self.lineEdit_correo.text().strip()
        contraseña = self.lineEdit_password.text()
        rol = self.comboBox_rol.currentText()
        dni = self.lineEdit_dni.text().strip()
        telefono = self.lineEdit_telefono.text().strip()
        tui = self.lineEdit_tui.text().strip() if self.lineEdit_tui.isVisible() else None
        grado = self.lineEdit_grado.text().strip() if self.lineEdit_grado.isVisible() else None
        especialidad = self.lineEdit_especialidad.text().strip() if self.lineEdit_especialidad.isVisible() else None

        if rol == "Selecciona un rol" or not all([nombre, apellido, correo, contraseña, dni, telefono]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor, completa todos los campos obligatorios.")
            return

        user = UserVo(
            idUser=None,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contraseña,
            rol=rol,
            tui=tui or None,
            dni=dni,
            telefono=telefono,
            fecha_alta=None,
            activo=True
        )

        bo = BussinessObject()
        resultado = bo.registrarUsuario(user)

        if resultado:
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
            self.close()
            if self.callback_volver:
                self.callback_volver()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el usuario.")
