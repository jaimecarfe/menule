from PyQt5.QtWidgets import QMessageBox
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorAdmin import ControladorAdmin
from src.vista.administrador.AdminPanel import AdminPanel
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/AdminPanel.ui")

class GestionUsuarios(VentanaBase, AdminPanel, Form):
    def __init__(self, usuario):
        super().__init__()
        self.setupUi(self)
        self.usuario = usuario
        self._controlador = ControladorAdmin()
        self.btnAgregarUsuario.clicked.connect(self.agregar_usuario)
        self.btnEliminarUsuario.clicked.connect(self.eliminar_usuario_seleccionado)

    def agregar_usuario(self, usuario):
        respuesta = QMessageBox.question(
            self,
            "Agregar Usuario",
            f"¿Estás seguro de que deseas agregar un usuario?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            self._controlador.agregar_usuario(usuario)
            self._controlador.cargar_usuarios_en_tabla()
            QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")

    def eliminar_usuario_seleccionado(self):
        fila_seleccionada = self.tablaUsuarios.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un usuario para eliminar.")
            return

        usuario_id = int(self.tablaUsuarios.item(fila_seleccionada, 0).text())
        respuesta = QMessageBox.question(
            self,
            "Eliminar Usuario",
            f"¿Estás seguro de que deseas eliminar el usuario con ID {usuario_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            self._controlador.eliminar_usuario(usuario_id)
            self._controlador.cargar_usuarios_en_tabla()
            QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")