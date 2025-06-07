from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from src.controlador.ControladorComedor import ControladorComedor

class ProcesarPedidos(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.controlador = ControladorComedor(usuario_actual)
        self.setWindowTitle("Pedidos Confirmados")
        self.setGeometry(300, 300, 800, 400)

        layout = QVBoxLayout()
        self.label = QLabel("Reservas confirmadas:")
        layout.addWidget(self.label)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID Reserva", "Fecha", "Correo", "Platos"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_pedidos()

    def cargar_pedidos(self):
        reservas = self.controlador.obtener_reservas_confirmadas()
        self.tabla.setRowCount(len(reservas))

        for i, (id_reserva, fecha, correo, platos) in enumerate(reservas):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(id_reserva)))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(fecha)))
            self.tabla.setItem(i, 2, QTableWidgetItem(correo))
            self.tabla.setItem(i, 3, QTableWidgetItem(platos))
