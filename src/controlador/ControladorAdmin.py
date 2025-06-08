from src.controlador.ControladorUsuarios import ControladorUsuarios
from src.controlador.ControladorPagos import ControladorPagos
from src.controlador.ControladorReservas import ControladorReservas
from src.controlador.ControladorConfiguracion import ControladorConfiguracion
from src.controlador.ControladorIncidencias import ControladorIncidencias
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

    def obtener_usuarios_para_tabla(self):
        usuarios = self.usuario_ctrl.listar_usuarios()
        datos = []
        for usuario in usuarios:
            datos.append([
                str(usuario.idUser),
                usuario.nombre,
                usuario.apellido,
                usuario.correo,
                usuario.rol,
                "Sí" if usuario.activo else "No"
            ])
        return datos

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
    
    def obtener_pagos_para_tabla(self):
        pagos = self.pago_ctrl.obtener_todos_los_pagos()
        datos = []
        for pago in pagos:
            datos.append([
                str(pago.id_pago),
                str(pago.id_usuario),
                str(pago.id_reserva),
                str(pago.monto),
                pago.metodo,
                str(pago.fecha_pago)
            ])
        return datos
    
    def obtener_reservas_para_tabla(self):
        reservas = self.reserva_ctrl.obtener_todas_las_reservas()
        datos = []
        for reserva in reservas:
            datos.append([
                str(reserva.id_reserva),
                str(reserva.id_usuario),
                str(reserva.id_menu),
                str(reserva.fecha_reserva)
            ])
        return datos
    
    def responder_incidencia(self, id_incidencia, respuesta, fecha):
        return self.incidencia_ctrl.responder_incidencia(id_incidencia, respuesta, fecha)