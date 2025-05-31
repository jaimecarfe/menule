from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from src.vista.VentanaBase import VentanaBase
from src.modelo.vo.UserVo import UserVo
from datetime import date
from src.modelo.BussinessObject import BussinessObject

Form, Window = uic.loadUiType("src/vista/ui/VistaRegistro.ui")

class Registro(VentanaBase, Form):
    def __init__(self, volver_a=None):
        super().__init__()
        self.setupUi(self)
        self._controlador = BussinessObject()
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
        
        if rol == "estudiante" and not tui:
            QMessageBox.warning(self, "Campo obligatorio", "El campo TUI es obligatorio para estudiantes.")
            return
        
        if rol in ["estudiante", "profesor"] and not grado:
            QMessageBox.warning(self, "Campo obligatorio", "El campo Grado Académico es obligatorio para estudiantes y profesores.")
            return
        
        if rol == "personal_comedor" and not especialidad:
            QMessageBox.warning(self, "Campo obligatorio", "El campo Especialidad es obligatorio para personal de comedor.")
            return
        
        if not dni or not telefono:
            QMessageBox.warning(self, "Campos obligatorios", "DNI y Teléfono son campos obligatorios.")
            return
        
        if len(dni) != 9 or not dni[:-1].isdigit() or not dni[-1].isalpha():
            QMessageBox.warning(self, "DNI inválido", "El DNI debe tener 8 dígitos seguidos de una letra.")
            return
        
        if len(telefono) < 9 or not telefono.isdigit():
            QMessageBox.warning(self, "Teléfono inválido", "El teléfono debe tener al menos 9 dígitos.")
            return
        
        if self._controlador.find_user_by_email(correo):
            QMessageBox.warning(self, "Correo existente", "Ya existe un usuario con este correo electrónico.")
            return
        
        if correo.count('@') != 1 or correo.count('.') < 1:
            QMessageBox.warning(self, "Correo inválido", "El correo electrónico debe tener un formato válido.")
            return
        
        if len(contrasena) < 6:
            QMessageBox.warning(self, "Contraseña débil", "La contraseña debe tener al menos 6 caracteres.")
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

        if self._controlador.registrarUsuario(user):
            QMessageBox.information(self, "Registro exitoso", "Usuario registrado correctamente.")
            self.close()
            if self._ventana_anterior:
                self._ventana_anterior.showNormal()
                self._ventana_anterior.showMaximized()

    def volver(self):
        self.close()
        if self._ventana_anterior:
            self._ventana_anterior.showFullScreen()