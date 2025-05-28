from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon
import os
from src.controlador.ControladorEstadisticas import ControladorEstadisticas

class VentanaEstadisticas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon(os.path.abspath("src/vista/logo/logo.png")))
        self.setWindowTitle("Estadísticas del sistema")

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.selector_tipo = QComboBox()
        self.selector_tipo.addItems(['Pagos', 'Incidencias', 'Menús', 'Reservas'])
        layout.addWidget(QLabel("Tipo de estadística:"))
        layout.addWidget(self.selector_tipo)

        self.label_estado = QLabel("")
        layout.addWidget(self.label_estado)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.controlador = ControladorEstadisticas(self)
        self.selector_tipo.currentTextChanged.connect(self.on_tipo_cambiado)

        # Cargar la primera estadística por defecto
        self.on_tipo_cambiado(self.selector_tipo.currentText())

    def on_tipo_cambiado(self, tipo):
        self.controlador.cargar_estadisticas(tipo)

    def mostrar_estadisticas(self, estadistica_vo):
        self.label_estado.setText("")
        datos = estadistica_vo.datos
        self.tabla.clear()
        self.tabla.setRowCount(0)
        if estadistica_vo.tipo == 'Pagos':
            self.tabla.setColumnCount(2)
            self.tabla.setHorizontalHeaderLabels(['Fecha', 'Total Pagado'])
        elif estadistica_vo.tipo == 'Incidencias':
            self.tabla.setColumnCount(2)
            self.tabla.setHorizontalHeaderLabels(['Fecha', 'Total Incidencias'])
        elif estadistica_vo.tipo == 'Menus':
            self.tabla.setColumnCount(2)
            self.tabla.setHorizontalHeaderLabels(['Fecha', 'Total Menús'])
        elif estadistica_vo.tipo == 'Reservas':
            self.tabla.setColumnCount(2)
            self.tabla.setHorizontalHeaderLabels(['Fecha', 'Total Reservas'])

        if not datos:
            self.label_estado.setText("Sin datos para mostrar.")
            return

        self.tabla.setRowCount(len(datos))
        for i, fila in enumerate(datos):
            for j, valor in enumerate(fila):
                self.tabla.setItem(i, j, QTableWidgetItem(str(valor)))

    def mostrar_mensaje(self, mensaje):
        self.label_estado.setText(mensaje)
        self.tabla.clear()
        self.tabla.setRowCount(0)

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)