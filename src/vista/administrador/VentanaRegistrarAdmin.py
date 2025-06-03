from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.modelo.vo.UserVo import UserVo
from src.modelo.BussinessObject import BussinessObject
from PyQt5.QtWidgets import QMessageBox

Form, Window = uic.loadUiType("./src/vista/ui/RegistrarAdmin.ui")

class VentanaRegistrarAdmin(QMainWindow, Form):
    def __init__(self, callback_volver=None):
        super().__init__()

        self._controlador = BussinessObject()

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
        
        if not self.validar_datos_registro(dni, correo, rol):
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

        
        resultado = self._controlador.registrarUsuario(user)

        if resultado:
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
            self.close()
            if self.callback_volver:
                self.callback_volver()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el usuario.")

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

        # Validar formato de DNI y letra
        import re
        patron_dni = re.match(r"^(\d{8})([A-Z])$", dni.upper())
        if not patron_dni:
            QMessageBox.warning(self, "DNI inválido", "El DNI debe tener 8 números y una letra en mayúscula.")
            return False

        numero_dni, letra_introducida = patron_dni.groups()
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        letra_correcta = letras[int(numero_dni) % 23]
        if letra_correcta != letra_introducida:
            QMessageBox.warning(self, "DNI inválido", f"El DNI no es válido.")
            return False

        if self._controlador.buscar_por_dni(dni):
            QMessageBox.warning(self, "DNI duplicado", "Ya existe un usuario registrado con este DNI.")
            return False

        return True
