# src/vista/administrador/GestionIncidencias.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from src.modelo.BussinessObject import BussinessObject

class PanelIncidenciasAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.modelo = BussinessObject()
        self.setWindowTitle("Gestión de Incidencias")
        self.setGeometry(100, 100, 1000, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Fecha", "Detalles", "Correo", "Estado"])
        self.tabla.verticalHeader().setDefaultSectionSize(50)
        self.layout.addWidget(self.tabla)

        self.cargar_datos()

    def cargar_datos(self):
        incidencias = self.modelo.incidencia_dao.obtener_todas()
        self.tabla.setRowCount(len(incidencias))
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



        for i, inc in enumerate(incidencias):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(inc.id)))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(inc.fecha)))

            btn = QPushButton("Ver")
            btn.clicked.connect(lambda _, inc=inc: self.ver_detalles(inc))
            self.tabla.setCellWidget(i, 2, btn)

            self.tabla.setItem(i, 3, QTableWidgetItem(inc.correo))

            combo = QComboBox()
            estados_visibles = {"En proceso": "en_proceso", "Resuelta": "resuelta"}
            combo.addItems(estados_visibles.keys())
            # seleccionar valor actual correspondiente
            for visible, valor in estados_visibles.items():
                if valor == inc.estado:
                    combo.setCurrentText(visible)
            combo.currentTextChanged.connect(lambda visible, inc_id=inc.id: self.cambiar_estado(inc_id, estados_visibles[visible]))
            self.tabla.setCellWidget(i, 4, combo)

    def ver_detalles(self, incidencia):
        QMessageBox.information(self, "Detalles de la Incidencia",
                                f"Título: {incidencia.titulo}\n\nDescripción:\n{incidencia.descripcion}")

    def cambiar_estado(self, id_incidencia, nuevo_estado):
        self.modelo.incidencia_dao.actualizar_estado(id_incidencia, nuevo_estado)
        #QMessageBox.information(self, "Estado actualizado", f"Incidencia {id_incidencia} marcada como '{nuevo_estado}'")
