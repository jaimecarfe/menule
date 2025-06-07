from src.controlador.ControladorUsuarios import ControladorUsuarios
from src.controlador.ControladorPagos import ControladorPagos
from src.controlador.ControladorReservas import ControladorReservas
from src.controlador.ControladorConfiguracion import ControladorConfiguracion
from PyQt5.QtWidgets import QTableWidgetItem

class ControladorAdmin:
    def __init__(self, vista=None):
        self._vista = vista
        self.usuario_ctrl = ControladorUsuarios()
        self.pago_ctrl = ControladorPagos()
        self.reserva_ctrl = ControladorReservas()
        self.config_ctrl = ControladorConfiguracion()

    def obtener_usuarios(self):
        return self.usuario_ctrl.listar_usuarios()

    def cargar_usuarios_en_tabla(self):
        usuarios = self.usuario_ctrl.listar_usuarios()
        tabla = self._vista.tablaUsuarios

        tabla.setRowCount(len(usuarios))
        tabla.setColumnCount(6)
        tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Correo", "Rol", "Activo"])

        for fila, usuario in enumerate(usuarios):
            tabla.setItem(fila, 0, QTableWidgetItem(str(usuario.idUser)))
            tabla.setItem(fila, 1, QTableWidgetItem(usuario.nombre))
            tabla.setItem(fila, 2, QTableWidgetItem(usuario.apellido))
            tabla.setItem(fila, 3, QTableWidgetItem(usuario.correo))
            tabla.setItem(fila, 4, QTableWidgetItem(usuario.rol))
            tabla.setItem(fila, 5, QTableWidgetItem("Sí" if usuario.activo else "No"))

    def eliminar_usuario(self, user_id):
        return self.usuario_ctrl.eliminar_usuario(user_id)
    
    def dar_de_baja_usuario(self, user_id):
        return self.usuario_ctrl.dar_de_baja_usuario(user_id)

    def actualizar_usuario(self, id_usuario, campo, nuevo_valor):
        return self.usuario_ctrl.actualizar_usuario(id_usuario, campo, nuevo_valor)

    def obtener_configuraciones(self):
        return self.config_ctrl.obtener_configuraciones()

    def guardar_configuracion(self, clave, valor):
        return self.config_ctrl.guardar_configuracion(clave, valor)
    
    def obtener_pagos(self):
        return self.pago_ctrl.obtener_todos_los_pagos()
    
    def obtener_reservas(self):
        return self.reserva_ctrl.obtener_todas_las_reservas()
