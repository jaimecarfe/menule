from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHeaderView, QDialog
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem  # si usas tabla
from src.vista.comun.GenerarTicket import GenerarTicket
from src.controlador.ControladorEstudiante import ControladorEstudiante

class HistorialReservas(QDialog):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Historial de Reservas")
        self.controlador = ControladorEstudiante()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tablaReservas = QTableWidget()
        self.layout.addWidget(self.tablaReservas)
        self.tablaReservas.resizeColumnsToContents()
        self.tablaReservas.resizeRowsToContents()

        self.tablaReservas.setMinimumSize(800, 300)
        self.adjustSize()

        # Botón para generar ticket
        self.btnGenerarTicket = QPushButton("Generar Ticket")
        self.btnGenerarTicket.clicked.connect(self.abrir_ticket_para_reserva)
        self.layout.addWidget(self.btnGenerarTicket)
        self.ver_historial()
   


    def ver_historial(self):
        self.tablaReservas.setRowCount(0)
        reservas = self.controlador.obtener_reservas_estudiante(self.usuario.idUser)
        self.tablaReservas.setColumnCount(7)  
        self.tablaReservas.setHorizontalHeaderLabels([
            "ID Reserva", "ID Usuario", "ID Menú", "Fecha", "Fecha Cancelación", "Estado", "Motivo Cancelación"
        ])
        self.tablaReservas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for fila_idx, reserva in enumerate(reservas):
            self.tablaReservas.insertRow(fila_idx)
            self.tablaReservas.setItem(fila_idx, 0, QTableWidgetItem(str(reserva.id_reserva)))
            self.tablaReservas.setItem(fila_idx, 1, QTableWidgetItem(str(reserva.id_usuario)))
            self.tablaReservas.setItem(fila_idx, 2, QTableWidgetItem(str(reserva.id_menu)))
            self.tablaReservas.setItem(fila_idx, 3, QTableWidgetItem(str(reserva.fecha_reserva)))
            self.tablaReservas.setItem(fila_idx, 4, QTableWidgetItem(str(reserva.fecha_cancelacion)))
            self.tablaReservas.setItem(fila_idx, 5, QTableWidgetItem(str(reserva.estado)))
            self.tablaReservas.setItem(fila_idx, 6, QTableWidgetItem(str(reserva.motivo_cancelacion)))

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
