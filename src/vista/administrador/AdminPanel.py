from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorAdmin import ControladorAdmin
from PyQt5 import uic
from src.vista.administrador.Estadisticas import VentanaEstadisticas
from src.vista.administrador.VentanaRegistrarAdmin import VentanaRegistrarAdmin
from src.vista.comun.CambiarContrasena import CambiarContrasena


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
        self.btnCambiarContrasena.clicked.connect(self.abrir_cambio_contrasena)
        self.cargar_usuarios()

        self.tabEstadisticas = VentanaEstadisticas(self)
        self.tabPanel.addTab(self.tabEstadisticas, "Estadísticas")    

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
        usuarios = self._controlador._modelo.listarUsuarios()
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
                exito = self._controlador.eliminar_usuario(user_id)
                if exito:
                    QMessageBox.information(self, "Éxito", "Usuario eliminado.")
                    self.cargar_usuarios()
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

