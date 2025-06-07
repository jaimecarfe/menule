from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QFileDialog
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorAdmin import ControladorAdmin
from PyQt5 import uic
from src.vista.administrador.Estadisticas import VentanaEstadisticas
from src.vista.administrador.VentanaRegistrarAdmin import VentanaRegistrarAdmin
from src.vista.comun.CambiarContrasena import CambiarContrasena
from src.vista.personal_comedor.ModificarMenuConAlergenos import ModificarMenuConAlergenos
from src.vista.administrador.GestionIncidencias import PanelIncidenciasAdmin
from PyQt5.QtWidgets import QHeaderView 
from src.vista.administrador.MenuAdmin import MenuAdmin

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
        self.btnDescargarBD.clicked.connect(self.descargar_base_datos)
        self.cargar_usuarios()
        self.tablaUsuarios.cellChanged.connect(self.actualizar_usuario_en_bd)
        self.tabEstadisticas = VentanaEstadisticas(self)
        self.tabPanel.addTab(self.tabEstadisticas, "Estadísticas")
        self.btnModificarMenu.clicked.connect(self.abrir_modificar_menu)  
        self.panel_incidencias = PanelIncidenciasAdmin()
        self.tabPanel.addTab(self.panel_incidencias, "Incidencias")
        self.cargar_pagos()
        self.cargar_reservas()
        self.btnVerMenuAdmin.clicked.connect(self.abrir_menu_admin)

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
            self._callback_cerrar_sesion()
            self.close()

    def cargar_usuarios(self):
        """Obtiene todos los usuarios y los muestra en la tabla."""
        self.tablaUsuarios.setRowCount(0)
        self.tablaUsuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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
        self.mod_window = ModificarMenuConAlergenos(usuario_actual=self.usuario)
        self.mod_window.show()

    '''
    def abrir_panel_incidencias(self):
        self.ventana_incidencias = AdminPanel()
        self.ventana_incidencias.show()
    '''

    def cargar_pagos(self):
        self.tablaPagos.setRowCount(0)
        pagos = self._controlador.obtener_pagos()
        self.tablaPagos.setColumnCount(8)
        self.tablaPagos.setHorizontalHeaderLabels([
            "ID Pago", "ID Usuario", "ID Reserva", "Monto", "Método",
            "Fecha de Pago", "Descuento", "Estado"
        ])
        self.tablaPagos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for fila_idx, pago in enumerate(pagos):
            self.tablaPagos.insertRow(fila_idx)
            self.tablaPagos.setItem(fila_idx, 0, QTableWidgetItem(str(pago.id_pago)))
            self.tablaPagos.setItem(fila_idx, 1, QTableWidgetItem(str(pago.id_usuario)))
            self.tablaPagos.setItem(fila_idx, 2, QTableWidgetItem(str(pago.id_reserva)))
            self.tablaPagos.setItem(fila_idx, 3, QTableWidgetItem(str(pago.monto)))
            self.tablaPagos.setItem(fila_idx, 4, QTableWidgetItem(pago.metodo))
            self.tablaPagos.setItem(fila_idx, 5, QTableWidgetItem(str(pago.fecha_pago)))
            self.tablaPagos.setItem(fila_idx, 6, QTableWidgetItem(str(pago.descuento)))
            self.tablaPagos.setItem(fila_idx, 7, QTableWidgetItem(pago.estado))
            #self.tablaPagos.setItem(fila_idx, 8, QTableWidgetItem(str(pago.transaccion_id) if pago.transaccion_id else ""))

    def cargar_reservas(self):
        self.tablaReservas.setRowCount(0)
        reservas = self._controlador.obtener_reservas()
        self.tablaReservas.setColumnCount(6)
        self.tablaReservas.setHorizontalHeaderLabels([
            "ID Reserva", "ID Usuario", "ID Menú", "Fecha", "Fecha de Cancelación", "Motivo de Cancelación"
        ])
        self.tablaReservas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for fila_idx, reserva in enumerate(reservas):
            self.tablaReservas.insertRow(fila_idx)
            self.tablaReservas.setItem(fila_idx, 0, QTableWidgetItem(str(reserva.id_reserva)))
            self.tablaReservas.setItem(fila_idx, 1, QTableWidgetItem(str(reserva.id_usuario)))
            self.tablaReservas.setItem(fila_idx, 2, QTableWidgetItem(str(reserva.id_menu)))
            self.tablaReservas.setItem(fila_idx, 3, QTableWidgetItem(str(reserva.fecha_reserva)))
            self.tablaReservas.setItem(fila_idx, 4, QTableWidgetItem(str(reserva.fecha_cancelacion)))
            self.tablaReservas.setItem(fila_idx, 5, QTableWidgetItem(str(reserva.motivo_cancelacion)))

    def abrir_menu_admin(self):
        self.menu_admin_window = MenuAdmin(self.usuario, parent=self)
        self.menu_admin_window.show()
        
    def descargar_base_datos(self):
        try:
            ruta_destino, _ = QFileDialog.getSaveFileName(
                self, "Guardar copia de la base de datos...", "menule_backup.sql", "Archivos SQL (*.sql)"
            )
            if not ruta_destino:
                return
            resultado = self._controlador.descargar_base_datos(ruta_destino)
            if resultado.returncode == 0:
                QMessageBox.information(self, "Éxito", "Base de datos exportada correctamente.")
            else:
                raise Exception(resultado.stderr)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar la base de datos:\n{str(e)}")
