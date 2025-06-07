from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel
from src.vista.comun.GenerarTicket import GenerarTicket
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorEstudiante import ControladorEstudiante
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/ReservaComida.ui")

class ReservaComida(QMainWindow, Form):
    def __init__(self, usuario, parent=None, primero=None, segundo=None, postre=None):
        super().__init__(parent)
        self.usuario = usuario
        self.setupUi(self)
        self.controlador = ControladorEstudiante()
        self.setWindowTitle("Reservar Comida")

        # Mostrar resumen
        if primero:
            self.labelSeleccionPrimero.setText(f"Primero: {primero}")
        if segundo:
            self.labelSeleccionSegundo.setText(f"Segundo: {segundo}")
        if postre:
            self.labelSeleccionPostre.setText(f"Postre: {postre}")

        # Menú simulado
        self.menus_disponibles = self.controlador.obtener_menus_disponibles()
        for menu in self.menus_disponibles:
            self.combo_menu.addItem(f"{menu['fecha']} - {menu['tipo']}", userData=menu['id_menu'])

        # Conectar botones
        self.btn_reservar.clicked.connect(self.realizar_reserva)
        self.btn_generar_ticket.clicked.connect(self.generar_ticket)
        self.btn_volver.clicked.connect(self.volver)

    def realizar_reserva(self):
        fecha = self.combo_menu.currentText().split(" - ")[0]  # o el dato correcto según tu combo
        id_reserva = self.controlador.hacer_reserva(self.usuario.idUser, fecha)
        if id_reserva:
            QMessageBox.information(self, "Reserva hecha", "Reserva registrada con éxito.")
            # Importa PagoWindow si hace falta
            from src.vista.comun.PagoWindow import PagoWindow
            self.ventana_pago = PagoWindow(self.usuario, precio=5.5, metodo="tui", callback_pago_exitoso=None, id_reserva=id_reserva)
            self.ventana_pago.show()
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