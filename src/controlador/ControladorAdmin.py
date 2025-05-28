from src.modelo.BussinessObject import BussinessObject
from PyQt5.QtWidgets import QTableWidgetItem
from src.modelo.dao.UserDao import UserDao
from src.modelo.dao.ConfiguracionDao import ConfiguracionDao

class ControladorAdmin:
    def __init__(self, vista):
        self._vista = vista
        self._modelo = BussinessObject()
        self.cargar_usuarios_en_tabla()

    def cargar_usuarios_en_tabla(self):
        usuarios = self._modelo.listarUsuarios()
        tabla = self._vista.tablaUsuarios

        tabla.setRowCount(len(usuarios))
        tabla.setColumnCount(5)
        tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Correo", "Rol", "Activo"])

        for fila, usuario in enumerate(usuarios):
            tabla.setItem(fila, 0, QTableWidgetItem(str(usuario.idUser)))
            tabla.setItem(fila, 1, QTableWidgetItem(usuario.nombre))
            tabla.setItem(fila, 2, QTableWidgetItem(usuario.apellido))
            tabla.setItem(fila, 3, QTableWidgetItem(usuario.correo))
            tabla.setItem(fila, 4, QTableWidgetItem(usuario.rol))
            tabla.setItem(fila, 5, QTableWidgetItem("Sí" if usuario.activo else "No"))

    def eliminar_usuario(self, user_id):
        """
        Llama al DAO para eliminar lógicamente un usuario.
        :param user_id: ID del usuario a eliminar
        :return: True si éxito, False si error
        """
        dao = UserDao()
        return dao.eliminar_usuario_logico(user_id)
    
    def obtener_configuraciones(self):
        dao = ConfiguracionDao()
        return dao.obtener_configuraciones()

    def guardar_configuracion(self, clave, valor):
        dao = ConfiguracionDao()
        return dao.guardar_configuracion(clave, valor)
