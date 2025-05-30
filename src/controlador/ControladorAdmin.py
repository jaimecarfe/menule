from src.modelo.BussinessObject import BussinessObject
from PyQt5.QtWidgets import QTableWidgetItem

class ControladorAdmin:
    def __init__(self, vista=None):
        self._vista = vista
        self._modelo = BussinessObject()
    
    def obtener_usuarios(self):
        return self._modelo.listarUsuarios()

    def cargar_usuarios_en_tabla(self):
        usuarios = self._modelo.listarUsuarios()
        tabla = self._vista.tablaUsuarios

        tabla.setRowCount(len(usuarios))
        tabla.setColumnCount(6)
        tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Correo", "Rol", "Activo"])

        for fila, usuario in enumerate(usuarios):
            tabla.setItem(fila, 0, QTableWidgetItem(str(usuario.idUser)))      # ID
            tabla.setItem(fila, 1, QTableWidgetItem(usuario.nombre))           # Nombre
            tabla.setItem(fila, 2, QTableWidgetItem(usuario.apellido))         # Apellido
            tabla.setItem(fila, 3, QTableWidgetItem(usuario.correo))           # Correo
            tabla.setItem(fila, 4, QTableWidgetItem(usuario.rol))              # Rol
            tabla.setItem(fila, 5, QTableWidgetItem("Sí" if usuario.activo else "No"))  # Activo
            
    def eliminar_usuario(self, user_id):
        return self._modelo.eliminarUsuario(user_id)
    
    def dar_de_baja_usuario(self, user_id):
        return self._modelo.darDeBajaUsuario(user_id)

    def actualizar_usuario(self, id_usuario, campo, nuevo_valor):
        return self._modelo.actualizarUsuario(id_usuario, campo, nuevo_valor)

    def obtener_configuraciones(self):
        return self._modelo.obtenerConfiguraciones()

    def guardar_configuracion(self, clave, valor):
        return self._modelo.guardarConfiguracion(clave, valor)