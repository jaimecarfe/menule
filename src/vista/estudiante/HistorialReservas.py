from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem  # si usas tabla
from src.vista.comun.GenerarTicket import GenerarTicket

class HistorialReservas(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Historial de Reservas")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tablaReservas = QTableWidget()
        self.tablaReservas.setColumnCount(4)  # ajusta según tus columnas
        self.tablaReservas.setHorizontalHeaderLabels(["ID", "Fecha", "Total", "Estado"])
        self.layout.addWidget(self.tablaReservas)

        # Botón para generar ticket
        self.btnGenerarTicket = QPushButton("Generar Ticket")
        self.btnGenerarTicket.clicked.connect(self.abrir_ticket_para_reserva)
        self.layout.addWidget(self.btnGenerarTicket)

        self.cargar_reservas()

    def cargar_reservas(self):
        # Esto es un ejemplo: debes cargar tus datos reales desde DAO
        reservas_ejemplo = [
            {"id": 1, "fecha": "2024-05-01", "total": 8.50, "estado": "confirmada"},
            {"id": 2, "fecha": "2024-05-02", "total": 6.00, "estado": "cancelada"},
        ]

        self.tablaReservas.setRowCount(len(reservas_ejemplo))

        for fila, reserva in enumerate(reservas_ejemplo):
            self.tablaReservas.setItem(fila, 0, QTableWidgetItem(str(reserva["id"])))
            self.tablaReservas.setItem(fila, 1, QTableWidgetItem(reserva["fecha"]))
            self.tablaReservas.setItem(fila, 2, QTableWidgetItem(f"{reserva['total']} €"))
            self.tablaReservas.setItem(fila, 3, QTableWidgetItem(reserva["estado"]))

    def obtener_id_reserva_seleccionada(self):
        fila = self.tablaReservas.currentRow()
        if fila == -1:
            return None
        return self.tablaReservas.item(fila, 0).text()

    def abrir_ticket_para_reserva(self):
        id_reserva = self.obtener_id_reserva_seleccionada()
        if id_reserva:
            self.ticket_window = GenerarTicket(id_reserva)
            self.ticket_window.show()
        else:
            QMessageBox.warning(self, "Selecciona una reserva", "Selecciona una fila de la tabla para generar el ticket.")
