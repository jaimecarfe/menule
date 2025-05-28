from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorAdmin import ControladorAdmin
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/AdminPanel.ui")

class AdminPanel(VentanaBase, Form):
    def __init__(self, usuario):
        super().__init__()
        self.setupUi(self)
        self.usuario = usuario
        self._controlador = ControladorAdmin(self)
        self._callback_cerrar_sesion = None
        self.btnCerrarSesion.clicked.connect(self.confirmar_cerrar_sesion)
        self.btnEliminarUsuario.clicked.connect(self.eliminar_usuario_seleccionado)
        self.cargar_usuarios()

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
