from PyQt5.QtWidgets import QMainWindow, QMessageBox
from src.vista.comun.GenerarTicket import GenerarTicket
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorEstudiante import ControladorEstudiante
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/ReservaComida.ui")

class ReservaComida(QMainWindow, Form):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self.setupUi(self)
        self.controlador = ControladorEstudiante()
        self.setWindowTitle("Reservar Comida")

        # Cargar menús simulados del controlador
        self.menus_disponibles = self.controlador.obtener_menus_disponibles()
        for menu in self.menus_disponibles:
            self.combo_menu.addItem(f"{menu['fecha']} - {menu['tipo']}", userData=menu['id_menu'])

        # Conectar botones
        self.btn_reservar.clicked.connect(self.realizar_reserva)
        self.btn_generar_ticket.clicked.connect(self.generar_ticket)
        self.btn_volver.clicked.connect(self.volver)

    def realizar_reserva(self):
        id_menu = self.combo_menu.currentData()
        exito = self.controlador.hacer_reserva(self.usuario.idUser, id_menu)
        if exito:
            QMessageBox.information(self, "Reserva hecha", "Reserva registrada con éxito.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la reserva.")

    def abrir_ticket(self):
        id_reserva = self.controlador.obtener_ultima_reserva_id(self.usuario.idUser)
        if id_reserva:
            self.ticket_window = GenerarTicket(id_reserva)
            self.ticket_window.show()
        else:
            QMessageBox.warning(self, "Sin reserva", "No se encontró ninguna reserva activa.")

    def generar_ticket(self):
        id_reserva = self.controlador.obtener_ultima_reserva_id(self.usuario.idUser)
        if id_reserva:
            self.ticket_window = GenerarTicket(id_reserva)
            if hasattr(self.ticket_window, "generar_pdf"):
                self.ticket_window.generar_pdf()
                QMessageBox.information(self, "Ticket generado", "El ticket se ha generado correctamente.")
            else:
                self.ticket_window.show()
        else:
            QMessageBox.warning(self, "Sin reserva", "No se encontró ninguna reserva activa para generar ticket.")

    def volver(self):
        self.close()