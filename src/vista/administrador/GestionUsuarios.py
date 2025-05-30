from PyQt5.QtWidgets import QMessageBox
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorAdmin import ControladorAdmin
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/AdminPanel.ui")

class GestionUsuarios(VentanaBase, Form):
    def __init__(self, usuario):
        super().__init__()
        self.setupUi(self)
        self.usuario = usuario
        self._controlador = ControladorAdmin()
        self.btnAgregarUsuario.clicked.connect(self.agregar_usuario)
        self.btnEliminarUsuario.clicked.connect(self.eliminar_usuario_seleccionado)
        self.cargar_usuarios_en_tabla()

    def cargar_usuarios_en_tabla(self):
        usuarios = self._controlador.obtener_usuarios()
        self.tablaUsuarios.setRowCount(0)
        for fila_idx, usuario in enumerate(usuarios):
            self.tablaUsuarios.insertRow(fila_idx)
            self.tablaUsuarios.setItem(fila_idx, 0, QTableWidgetItem(str(usuario.idUser)))
            self.tablaUsuarios.setItem(fila_idx, 1, QTableWidgetItem(usuario.nombre))
            self.tablaUsuarios.setItem(fila_idx, 2, QTableWidgetItem(usuario.apellido))
            self.tablaUsuarios.setItem(fila_idx, 3, QTableWidgetItem(usuario.correo))
            self.tablaUsuarios.setItem(fila_idx, 4, QTableWidgetItem(usuario.rol))
            self.tablaUsuarios.setItem(fila_idx, 5, QTableWidgetItem("Sí" if usuario.activo else "No"))

    def agregar_usuario(self):
        # Abre un formulario para crear usuario, captura los datos y pásalos al controlador
        # Por ejemplo:
        datos_usuario = self.abrir_formulario_nuevo_usuario()
        if datos_usuario:
            respuesta = QMessageBox.question(
                self,
                "Agregar Usuario",
                "¿Estás seguro de que deseas agregar un usuario?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                exito = self._controlador.agregar_usuario(datos_usuario)
                if exito:
                    self.cargar_usuarios_en_tabla()
                    QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
                else:
                    QMessageBox.critical(self, "Error", "No se pudo agregar el usuario.")

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
            exito = self._controlador.eliminar_usuario(usuario_id)
            if exito:
                self.cargar_usuarios_en_tabla()
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el usuario.")