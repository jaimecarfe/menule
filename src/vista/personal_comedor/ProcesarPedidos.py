from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QHeaderView
from src.controlador.ControladorProcesarPedidos import ControladorProcesarPedidos

class ProcesarPedidos(QWidget):
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Procesar Pedidos")
        self.setMinimumSize(800, 500)
        self._controlador = ControladorProcesarPedidos()

        self.layout = QVBoxLayout()
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "ID Reserva", "Correo", "Menú (3 platos)", "Acciones"])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.tabla)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        self.layout.addWidget(self.btn_actualizar)

        self.setLayout(self.layout)
        self.cargar_datos()
        self.tabla.cellClicked.connect(self.mostrar_detalle_menu)

    def cargar_datos(self):
        reservas = self._controlador.obtener_reservas()
        self.tabla.setRowCount(0)
        for i, reserva in enumerate(reservas):
            self.tabla.insertRow(i)
            self.tabla.setItem(i, 0, QTableWidgetItem(str(reserva['fecha'])))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(reserva['id_reserva'])))
            self.tabla.setItem(i, 2, QTableWidgetItem(reserva['correo']))
            item_menu = QTableWidgetItem(reserva['menu'])
            item_menu.setToolTip("Haz clic para ver detalles")
            self.tabla.setItem(i, 3, item_menu)

            widget = QWidget()
            hbox = QHBoxLayout()
            btn_recogida = QPushButton("Recogida")
            btn_cancelar = QPushButton("Cancelar")

            if reserva['estado_bit'] == 1:
                btn_recogida.setStyleSheet("background-color: lightgreen;")
            elif reserva['estado_bit'] == 0:
                btn_cancelar.setStyleSheet("background-color: lightcoral;")

            btn_recogida.clicked.connect(lambda _, r=reserva['id_reserva'], b1=btn_recogida, b2=btn_cancelar: self.actualizar_estado(r, 1, b1, b2))
            btn_cancelar.clicked.connect(lambda _, r=reserva['id_reserva'], b1=btn_recogida, b2=btn_cancelar: self.actualizar_estado(r, 0, b1, b2))

            hbox.addWidget(btn_recogida)
            hbox.addWidget(btn_cancelar)
            hbox.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(hbox)
            self.tabla.setCellWidget(i, 4, widget)

        self.tabla.resizeColumnsToContents()
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def actualizar_estado(self, id_reserva, bit, boton_recogida, boton_cancelar):
        try:
            self._controlador.actualizar_estado(id_reserva, bit)
            if bit == 1:
                boton_recogida.setStyleSheet("background-color: lightgreen;")
                boton_cancelar.setStyleSheet("")
            else:
                boton_cancelar.setStyleSheet("background-color: lightcoral;")
                boton_recogida.setStyleSheet("")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar la reserva:\n{e}")

    def mostrar_detalle_menu(self, row, column):
        if column == 3:  # Menú (3 platos)
            item = self.tabla.item(row, column)
            if item:
                texto = item.text()
                platos = [p.strip() for p in texto.split(",")]
                mensaje = "\n".join(platos)
                QMessageBox.information(self, "Detalle del menú", mensaje)