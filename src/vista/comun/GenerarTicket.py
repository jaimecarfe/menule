from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox
from src.controlador.ControladorTickets import ControladorTickets
from src.vista.visitante.IntroducirCorreoDialog import IntroducirCorreoDialog

class GenerarTicket(QWidget):
    def __init__(self, id_reserva):
        super().__init__()
        self.id_reserva = id_reserva
        self.controlador = ControladorTickets()

        self.setStyleSheet("""
            QWidget {
            background-color: #e6f2ff;
            font-family: Arial;
            font-size: 14px;
        }
        QLabel {
            color: #005c99;
            font-weight: bold;
        }
        QLineEdit {
            border: 1px solid #80bfff;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QPushButton {
            background-color: #00cc99;
            color: white;
            border-radius: 10px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #009973;
        }
        """)

        self.setWindowTitle("Ticket de Reserva")
        self.setFixedSize(220, 120)

        self.btn_generar = QPushButton("Generar PDF")
        self.btn_enviar = QPushButton("Enviar por correo")

        self.btn_generar.clicked.connect(self.generar_pdf)
        self.btn_enviar.clicked.connect(self.enviar_por_correo)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_generar)
        layout.addWidget(self.btn_enviar)
        self.setLayout(layout)

        # Si es visitante, ocultar botón de correo y abrir diálogo directamente
        if self.controlador.es_reserva_de_visitante(self.id_reserva):
            self.btn_enviar.setVisible(False)
            self._pedir_y_enviar_correo_a_visitante()

    def generar_pdf(self):
        ruta = self.controlador.generar_pdf_ticket(self.id_reserva)
        if ruta:
            QMessageBox.information(self, "PDF generado", f"Ticket guardado en:\n{ruta}")
        else:
            QMessageBox.warning(self, "Error", "No se pudo generar el ticket.")

    def enviar_por_correo(self):
        datos = self.controlador.obtener_datos_ticket(self.id_reserva)
        if not datos or not datos[2] or datos[2].strip() == "":
            QMessageBox.warning(self, "Sin correo", "No se puede enviar el ticket: el correo no está disponible.")
            return

        correo = datos[2]
        exito, error = self.controlador.enviar_ticket_por_correo(self.id_reserva, correo)
        if exito:
            QMessageBox.information(self, "Enviado", "Ticket enviado correctamente.")
        else:
            QMessageBox.warning(self, "Error", f"No se pudo enviar el ticket: {error}")

    def _pedir_y_enviar_correo_a_visitante(self):
        dialog = IntroducirCorreoDialog(self)
        if dialog.exec_():
            correo = dialog.correo
            exito, error = self.controlador.enviar_ticket_por_correo(self.id_reserva, correo)
            if exito:
                QMessageBox.information(self, "Enviado", "Ticket enviado correctamente.")
            else:
                QMessageBox.warning(self, "Error", f"No se pudo enviar el ticket: {error}")