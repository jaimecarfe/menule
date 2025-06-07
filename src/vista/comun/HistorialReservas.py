from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QMessageBox, QHeaderView, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from src.vista.comun.GenerarTicket import GenerarTicket
from src.controlador.ControladorEstudiante import ControladorEstudiante

class HistorialReservas(QDialog):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Historial de Reservas")
        self.setMinimumWidth(900)
        self.setMinimumHeight(420)
        self.controlador = ControladorEstudiante()

        self.layout = QVBoxLayout(self)

        # Tabla
        self.tablaReservas = QTableWidget()
        self.tablaReservas.setColumnCount(5)
        self.tablaReservas.setHorizontalHeaderLabels([
            "ID Reserva", "ID Usuario", "ID Menú", "Fecha", "Estado"
        ])
        self.tablaReservas.setSelectionBehavior(self.tablaReservas.SelectRows)
        self.tablaReservas.setSelectionMode(self.tablaReservas.SingleSelection)
        self.tablaReservas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablaReservas.verticalHeader().setVisible(False)
        self.tablaReservas.setAlternatingRowColors(True)
        self.tablaReservas.setStyleSheet("""
            QTableWidget {
                background-color: #f6f8fa;
                border: 1px solid #bdbdbd;
                font-size: 14px;
                gridline-color: #bbdefb;
            }
            QTableWidget::item:selected {
                background: #1976d2;
                color: white;
            }
            QHeaderView::section {
                background-color: #1976d2;
                color: white;
                font-weight: bold;
                font-size: 15px;
                padding: 6px;
                border: 1px solid #1565c0;
            }
        """)
        self.layout.addWidget(self.tablaReservas)

        # Botón para generar ticket
        self.btnGenerarTicket = QPushButton("Generar Ticket")
        self.btnGenerarTicket.setCursor(Qt.PointingHandCursor)
        self.btnGenerarTicket.setEnabled(False)
        self.btnGenerarTicket.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                padding: 10px 25px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 8px;
            }
            QPushButton:hover:!disabled {
                background-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #b0bec5;
                color: #eceff1;
            }
        """)
        self.btnGenerarTicket.clicked.connect(self.abrir_ticket_para_reserva)
        self.layout.addWidget(self.btnGenerarTicket)

        self.tablaReservas.itemSelectionChanged.connect(self.on_selection_changed)

        self.ver_historial()

    def ver_historial(self):
        self.tablaReservas.setRowCount(0)
        reservas = self.controlador.obtener_reservas_estudiante(self.usuario.idUser)
        self.tablaReservas.setColumnCount(5)  
        self.tablaReservas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for fila_idx, reserva in enumerate(reservas):
            self.tablaReservas.insertRow(fila_idx)
            self.tablaReservas.setItem(fila_idx, 0, QTableWidgetItem(str(reserva.id_reserva)))
            self.tablaReservas.setItem(fila_idx, 1, QTableWidgetItem(str(reserva.id_usuario)))
            self.tablaReservas.setItem(fila_idx, 2, QTableWidgetItem(str(reserva.id_menu)))
            self.tablaReservas.setItem(fila_idx, 3, QTableWidgetItem(str(reserva.fecha_reserva)))
            self.tablaReservas.setItem(fila_idx, 4, QTableWidgetItem(str(reserva.estado)))
        self.tablaReservas.resizeColumnsToContents()
        self.tablaReservas.resizeRowsToContents()

    def obtener_id_reserva_seleccionada(self):
        selected = self.tablaReservas.selectedItems()
        if not selected:
            return None
        row = self.tablaReservas.currentRow()
        return self.tablaReservas.item(row, 0).text() if row != -1 else None

    def on_selection_changed(self):
        self.btnGenerarTicket.setEnabled(self.tablaReservas.currentRow() != -1)

    def abrir_ticket_para_reserva(self):
        id_reserva = self.obtener_id_reserva_seleccionada()
        if id_reserva:
            self.ticket_window = GenerarTicket(id_reserva)
            self.ticket_window.show()
        else:
            QMessageBox.warning(self, "Selecciona una reserva", "Selecciona una fila de la tabla para generar el ticket.")