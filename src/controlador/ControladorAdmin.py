from src.controlador.ControladorUsuarios import ControladorUsuarios
from src.controlador.ControladorPagos import ControladorPagos
from src.controlador.ControladorReservas import ControladorReservas
from src.controlador.ControladorConfiguracion import ControladorConfiguracion
from src.controlador.ControladorIncidencias import ControladorIncidencias
from PyQt5.QtWidgets import QTableWidgetItem
import subprocess

class ControladorAdmin:
    def __init__(self, vista=None):
        self._vista = vista
        self.usuario_ctrl = ControladorUsuarios()
        self.pago_ctrl = ControladorPagos()
        self.reserva_ctrl = ControladorReservas()
        self.config_ctrl = ControladorConfiguracion()
        self.incidencia_ctrl = ControladorIncidencias()

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
    
    def responder_incidencia(self, id_incidencia, respuesta, fecha):
        return self.incidencia_ctrl.responder_incidencia(id_incidencia, respuesta, fecha)
    
    def descargar_base_datos(self, ruta_destino):
        usuario = "root"
        password = "Liverpool.840"
        nombre_bd = "menule"
        host = "localhost"
        comando = [
            "mysqldump",
            f"-u{usuario}",
            f"-p{password}",
            "-h", host,
            nombre_bd
        ]
        with open(ruta_destino, "w") as salida:
            resultado = subprocess.run(comando, stdout=salida, stderr=subprocess.PIPE, text=True)
        return resultado
