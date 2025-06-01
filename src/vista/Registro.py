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
        
        if not self.validar_datos_registro(dni, correo, rol):
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
            self._ventana_anterior.showFullScreen()
            
    def volver(self):
        self.close()
        if self._ventana_anterior:
            self._ventana_anterior.showFullScreen()

    def validar_datos_registro(self, dni, correo, rol):
        # Validar correo por rol
        dominios_validos = {
            "estudiante": "@estudiantes.unileon.es",
            "profesor": "@unileon.es",
            "personal_comedor": "@comedor.unileon.es",
            "administrador": "@menule.com",
        }

        if rol in dominios_validos:
            if not correo.endswith(dominios_validos[rol]):
                QMessageBox.warning(self, "Correo inválido",
                    f"El correo para rol '{rol}' no tiene la extensión correcta.")
                return False

        # Validar visitantes (solo para envío)
        if rol == "visitante":
            if not (correo.endswith("@gmail.com") or correo.endswith("@hotmail.com")):
                QMessageBox.warning(self, "Correo inválido",
                    "Los visitantes solo pueden usar correos @gmail.com o @hotmail.com")
                return False

        import re
        patron_dni = re.match(r"^(\d{8})([A-Z])$", dni.upper())
        if not patron_dni:
            QMessageBox.warning(self, "DNI inválido", "El DNI debe tener 8 números y una letra en mayúscula.")
            return False

        numero_dni, letra_introducida = patron_dni.groups()
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        letra_correcta = letras[int(numero_dni) % 23]
        if letra_correcta != letra_introducida:
            QMessageBox.warning(self, "DNI inválido", "El DNI no es válido.")
            return False

        if self._controlador.buscar_por_dni(dni):
            QMessageBox.warning(self, "DNI duplicado", "Ya existe un usuario registrado con este DNI.")
            return False

        return True
