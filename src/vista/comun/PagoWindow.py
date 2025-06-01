from PyQt5.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QPushButton, QMessageBox
from src.vista.comun.GenerarTicket import GenerarTicket

class PagoWindow(QWidget):
    def __init__(self, id_reserva, correo):
        super().__init__()
        self.id_reserva = id_reserva
        self.correo = correo
        self.setWindowTitle("Pago")

        layout = QVBoxLayout()
        self.radio_efectivo = QRadioButton("Efectivo")
        self.radio_tarjeta = QRadioButton("Tarjeta")
        self.btn_pagar = QPushButton("Pagar")
        self.btn_pagar.clicked.connect(self.confirmar_pago)

        layout.addWidget(self.radio_efectivo)
        layout.addWidget(self.radio_tarjeta)
        layout.addWidget(self.btn_pagar)
        self.setLayout(layout)

    def confirmar_pago(self):
        if not self.radio_efectivo.isChecked() and not self.radio_tarjeta.isChecked():
            QMessageBox.warning(self, "Selecciona un método", "Debes seleccionar un método de pago.")
            return

        metodo = "efectivo" if self.radio_efectivo.isChecked() else "tarjeta"
        QMessageBox.information(self, "Pago realizado", f"Pagado con {metodo}. Enviando ticket...")

        self.ticket = GenerarTicket(self.id_reserva)
        if hasattr(self.ticket, "enviar_ticket_por_correo_manual"):
            self.ticket.enviar_ticket_por_correo_manual(self.correo)
        self.ticket.show()
        self.close()
