from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from src.vista.VentanaBase import VentanaBase
from src.modelo.vo.UserVo import UserVo
from datetime import date
from src.utils.email_utils import enviar_correo
from src.utils import validador_usuario as val
import random
from src.vista.Login import Login
from src.controlador.ControladorPrincipal import ControladorPrincipal

Form, Window = uic.loadUiType("src/vista/ui/VistaRegistro.ui")

class Registro(VentanaBase, Form):
    def __init__(self, volver_a=None):
        super().__init__()
        self.setupUi(self)
        self._controlador = ControladorPrincipal(self)
        self._ventana_anterior = volver_a

        self.setWindowTitle("MenULE - Registro")
        self.pushButton_registrar.clicked.connect(self.on_registrar)
        self.pushButton_volver.clicked.connect(self.volver)
        self.comboBox_rol.currentIndexChanged.connect(self.on_rol_cambiado)
        self.on_rol_cambiado()

    def on_rol_cambiado(self):
        rol = self.comboBox_rol.currentText()
        self.lineEdit_grado.setVisible(rol in ["estudiante", "profesor"])
        self.lineEdit_especialidad.setVisible(rol == "personal_comedor")

    def on_registrar(self):
        nombre = self.lineEdit_nombre.text()
        apellido = self.lineEdit_apellido.text()
        correo = self.lineEdit_correo.text()
        contrasena = self.lineEdit_password.text()
        rol = self.comboBox_rol.currentText()
        tui = None
        if rol in ["estudiante", "profesor"]:
            prefijo = "E" if rol == "estudiante" else "P"
            tui = prefijo + ''.join(str(random.randint(0, 9)) for _ in range(8))
        grado = self.lineEdit_grado.text() if rol in ["estudiante", "profesor"] else None
        especialidad = self.lineEdit_especialidad.text() if rol == "personal_comedor" else None
        dni = self.lineEdit_dni.text()
        telefono = self.lineEdit_telefono.text()
        fecha_alta = date.today()

        # Validaciones simples
        if not all([nombre, apellido, correo, contrasena, rol]):
            QMessageBox.warning(self, "Campos obligatorios", "Completa todos los campos.")
            return
        if rol in ["estudiante", "profesor"] and not grado:
            QMessageBox.warning(self, "Falta grado", "El campo grado académico es obligatorio.")
            return
        if rol == "personal_comedor" and not especialidad:
            QMessageBox.warning(self, "Falta especialidad", "El campo especialidad es obligatorio.")
            return
        if not dni or len(dni) != 9 or not dni[:-1].isdigit() or not dni[-1].isalpha():
            QMessageBox.warning(self, "DNI inválido", "Debe tener 8 números y 1 letra.")
            return
        if not val.validar_dni(dni):
            QMessageBox.warning(self, "DNI inválido", "La letra del DNI no es válida.")
            return
        if not telefono.isdigit() or len(telefono) < 9:
            QMessageBox.warning(self, "Teléfono inválido", "Debe tener al menos 9 dígitos.")
            return
        if self._controlador.obtener_usuario_por_correo(correo):
            QMessageBox.warning(self, "Correo existente", "Ya existe un usuario con este correo.")
            return
        if not val.validar_correo_por_rol(correo, rol):
            QMessageBox.warning(self, "Correo inválido", f"El correo no es válido para el rol {rol}.")
            return
        if len(contrasena) < 6:
            QMessageBox.warning(self, "Contraseña débil", "Debe tener al menos 6 caracteres.")
            return
        if self._controlador.buscar_usuario_por_dni(dni):
            QMessageBox.warning(self, "DNI duplicado", "Ya existe un usuario registrado con este DNI.")
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
            try:
                asunto = "Registro exitoso en MenULE"
                mensaje = (
                    f"Hola {nombre} {apellido},\n\n"
                    f"Te has registrado exitosamente en MenULE con el rol de {rol}.\n\n"
                    f"Gracias por unirte a nuestra plataforma.\n\n"
                    f"Saludos,\nEl equipo de MenULE"
                )
                enviar_correo(correo, asunto, mensaje)
                QMessageBox.information(self, "Correo enviado", "Se ha enviado un correo de confirmación.")
            except Exception:
                QMessageBox.warning(self, "Error", "No se pudo enviar el correo.")
            QMessageBox.information(self, "Registro exitoso", "Usuario registrado correctamente.")
            self.close()
            if self._ventana_anterior:
                self._ventana_anterior.limpiar_campos()
                self._ventana_anterior.showFullScreen()

    def volver(self):
        self.close()
        if self._ventana_anterior:
            self._ventana_anterior.showFullScreen()
