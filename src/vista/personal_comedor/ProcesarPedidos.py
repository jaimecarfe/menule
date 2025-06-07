from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHBoxLayout, QHeaderView
)
from PyQt5.QtCore import Qt
from src.controlador.ControladorProcesarPedidos import ControladorProcesarPedidos

class ProcesarPedidos(QWidget):
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Procesar Pedidos")
        self.setMinimumSize(900, 550)
        self._controlador = ControladorProcesarPedidos()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "Fecha", "ID Reserva", "Correo", "Menú (3 platos)", "Acciones"
        ])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(self.tabla.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: #f8fafc;
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
                padding: 6px 0;
                border: 1px solid #1565c0;
            }
        """)
        self.layout.addWidget(self.tabla)

        # Botón actualizar
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setCursor(Qt.PointingHandCursor)
        self.btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                padding: 10px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 8px 0 18px 0;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        self.layout.addWidget(self.btn_actualizar, alignment=Qt.AlignRight)

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

            # Botones de acción
            widget = QWidget()
            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.setSpacing(6)

            btn_recogida = QPushButton("Recogida")
            btn_cancelar = QPushButton("Cancelar")

            btn_recogida.setCursor(Qt.PointingHandCursor)
            btn_cancelar.setCursor(Qt.PointingHandCursor)

            btn_recogida.setStyleSheet("""
                QPushButton {
                    background-color: #43a047;
                    color: white;
                    border-radius: 7px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 7px 14px;
                }
                QPushButton:hover { background-color: #388e3c; }
            """ if reserva['estado_bit'] == 1 else """
                QPushButton {
                    background-color: #e0e0e0;
                    color: #43a047;
                    border-radius: 7px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 7px 14px;
                }
                QPushButton:hover { background-color: #a5d6a7; }
            """)
            btn_cancelar.setStyleSheet("""
                QPushButton {
                    background-color: #e53935;
                    color: white;
                    border-radius: 7px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 7px 14px;
                }
                QPushButton:hover { background-color: #b71c1c; }
            """ if reserva['estado_bit'] == 0 else """
                QPushButton {
                    background-color: #e0e0e0;
                    color: #e53935;
                    border-radius: 7px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 7px 14px;
                }
                QPushButton:hover { background-color: #ffcdd2; }
            """)

            btn_recogida.clicked.connect(
                lambda _, r=reserva['id_reserva'], b1=btn_recogida, b2=btn_cancelar: self.actualizar_estado(r, 1, b1, b2)
            )
            btn_cancelar.clicked.connect(
                lambda _, r=reserva['id_reserva'], b1=btn_recogida, b2=btn_cancelar: self.actualizar_estado(r, 0, b1, b2)
            )

            hbox.addWidget(btn_recogida)
            hbox.addWidget(btn_cancelar)
            widget.setLayout(hbox)
            self.tabla.setCellWidget(i, 4, widget)

        self.tabla.resizeColumnsToContents()
        self.tabla.resizeRowsToContents()

    def actualizar_estado(self, id_reserva, bit, boton_recogida, boton_cancelar):
        try:
            self._controlador.actualizar_estado(id_reserva, bit)
            if bit == 1:
                boton_recogida.setStyleSheet("""
                    QPushButton {
                        background-color: #43a047;
                        color: white;
                        border-radius: 7px;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 7px 14px;
                    }
                    QPushButton:hover { background-color: #388e3c; }
                """)
                boton_cancelar.setStyleSheet("""
                    QPushButton {
                        background-color: #e0e0e0;
                        color: #e53935;
                        border-radius: 7px;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 7px 14px;
                    }
                    QPushButton:hover { background-color: #ffcdd2; }
                """)
            else:
                boton_cancelar.setStyleSheet("""
                    QPushButton {
                        background-color: #e53935;
                        color: white;
                        border-radius: 7px;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 7px 14px;
                    }
                    QPushButton:hover { background-color: #b71c1c; }
                """)
                boton_recogida.setStyleSheet("""
                    QPushButton {
                        background-color: #e0e0e0;
                        color: #43a047;
                        border-radius: 7px;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 7px 14px;
                    }
                    QPushButton:hover { background-color: #a5d6a7; }
                """)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar la reserva:\n{e}")

    def mostrar_detalle_menu(self, row, column):
        if column == 3:  # Menú (3 platos)
            item = self.tabla.item(row, column)
            if item:
                texto = item.text()
                platos = [p.strip() for p in texto.split(",")]
                mensaje = "\n".join(platos)
                QMessageBox.information(
                    self, "Detalle del menú", mensaje
                )