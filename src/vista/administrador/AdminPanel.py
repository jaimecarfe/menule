from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorAdmin import ControladorAdmin
from PyQt5 import uic
from src.vista.administrador.Estadisticas import VentanaEstadisticas
from src.vista.administrador.VentanaRegistrarAdmin import VentanaRegistrarAdmin
from src.vista.comun.CambiarContrasena import CambiarContrasena
from src.vista.comun.ModificarMenuConAlergenos import ModificarMenuConAlergenos



Form, Window = uic.loadUiType("./src/vista/ui/AdminPanel.ui")

class AdminPanel(VentanaBase, Form):
    def __init__(self, usuario):
        super().__init__()
        self.setupUi(self)
        self.usuario = usuario
        self._controlador = ControladorAdmin(self)
        self._controlador.cargar_usuarios_en_tabla()
        self._callback_cerrar_sesion = None
        self.btnCerrarSesion.clicked.connect(self.confirmar_cerrar_sesion)
        self.btnEliminarUsuario.clicked.connect(self.eliminar_usuario_seleccionado)
        self.btnAgregarUsuario.clicked.connect(self.abrir_ventana_registrar_admin)
        self.btnDarDeBaja.clicked.connect(self.dar_de_baja_usuario_seleccionado)
        self.btnCambiarContrasena.clicked.connect(self.abrir_cambio_contrasena)
        self.cargar_usuarios()
        self.tablaUsuarios.cellChanged.connect(self.actualizar_usuario_en_bd)
        self.tabEstadisticas = VentanaEstadisticas(self)
        self.tabPanel.addTab(self.tabEstadisticas, "Estadísticas")
        self.botonModificarMenu.clicked.connect(self.abrir_modificar_menu)  

    @property
    def callback_cerrar_sesion(self):
        return self._callback_cerrar_sesion

    @callback_cerrar_sesion.setter
    def callback_cerrar_sesion(self, callback):
        self._callback_cerrar_sesion = callback

    def confirmar_cerrar_sesion(self):
        respuesta = QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if respuesta == QMessageBox.Yes and self._callback_cerrar_sesion:
            self.close()
            self._callback_cerrar_sesion()

    def cargar_usuarios(self):
        """Obtiene todos los usuarios y los muestra en la tabla."""
        self.tablaUsuarios.setRowCount(0)
        usuarios = self._controlador.obtener_usuarios()
        for fila_idx, usuario in enumerate(usuarios):
            self.tablaUsuarios.insertRow(fila_idx)
            self.tablaUsuarios.setItem(fila_idx, 0, QTableWidgetItem(str(usuario.idUser)))
            self.tablaUsuarios.setItem(fila_idx, 1, QTableWidgetItem(usuario.nombre))
            self.tablaUsuarios.setItem(fila_idx, 2, QTableWidgetItem(usuario.apellido))
            self.tablaUsuarios.setItem(fila_idx, 3, QTableWidgetItem(usuario.correo))
            self.tablaUsuarios.setItem(fila_idx, 4, QTableWidgetItem(usuario.rol))
            self.tablaUsuarios.setItem(fila_idx, 5, QTableWidgetItem("Sí" if usuario.activo else "No"))

    def eliminar_usuario_seleccionado(self):
        fila = self.tablaUsuarios.currentRow()
        if fila >= 0:
            user_id = self.tablaUsuarios.item(fila, 0).text()
            confirmacion = QMessageBox.question(self, "Confirmar", "¿Deseas eliminar este usuario?")
            if confirmacion == QMessageBox.Yes:
                resultado = self._controlador.eliminar_usuario(user_id)
                if resultado is True:
                    QMessageBox.information(self, "Éxito", "Usuario eliminado.")
                    self.cargar_usuarios()
                elif resultado == "admin":
                    QMessageBox.warning(self, "No permitido", "No se puede eliminar un usuario administrador.")
                else:
                    QMessageBox.critical(self, "Error", "No se pudo eliminar el usuario.")

    def abrir_ventana_registrar_admin(self):
        def volver_y_recargar():
            self.show()
            self.cargar_usuarios()
        self.ventana_registro = VentanaRegistrarAdmin(callback_volver=volver_y_recargar)
        self.hide()
        self.ventana_registro.show() 
          
    def showEvent(self, event):
        super().showEvent(event)
        self._controlador.cargar_usuarios_en_tabla()

    def abrir_cambio_contrasena(self):
        self.ventana_cambio = CambiarContrasena(self.usuario)
        self.ventana_cambio.show()

    def actualizar_usuario_en_bd(self, fila, columna):
        if columna == 0:
            return  
        tabla = self.tablaUsuarios
        id_usuario = int(tabla.item(fila, 0).text())
        nuevo_valor = tabla.item(fila, columna).text()
        campos = ["dni","nombre", "apellido", "email", "tipo", "credencial_activa"]
        campo_bd = campos[columna]
        if campo_bd == "credencial_activa":
            nuevo_valor = nuevo_valor.strip().lower()
            if nuevo_valor in ["sí", "si", "true", "1"]:
                nuevo_valor = True
            else:
                nuevo_valor = False
        self._controlador.actualizar_usuario(id_usuario, campo_bd, nuevo_valor)

    def dar_de_baja_usuario_seleccionado(self):
        fila = self.tablaUsuarios.currentRow()
        if fila >= 0:
            user_id = self.tablaUsuarios.item(fila, 0).text()
            confirmacion = QMessageBox.question(
                self, "Confirmar", "¿Deseas dar de baja este usuario?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirmacion == QMessageBox.Yes:
                resultado = self._controlador.dar_de_baja_usuario(user_id)
                if resultado is True:
                    QMessageBox.information(self, "Éxito", "Usuario dado de baja correctamente.")
                    self.cargar_usuarios()
                elif resultado == "admin":
                    QMessageBox.warning(self, "No permitido", "No se puede dar de baja un administrador.")
                else:
                    QMessageBox.critical(self, "Error", "No se pudo dar de baja al usuario.")

    def abrir_modificar_menu(self):
        self.mod_window = ModificarMenuConAlergenos()
        self.mod_window.show()


