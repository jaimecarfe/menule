from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QDateEdit, QLineEdit, QPushButton,
    QMessageBox, QFormLayout, QCheckBox, QHBoxLayout
)
from PyQt5.QtCore import QDate
from src.modelo.dao.MenuDao import MenuDao

ALERGENOS = [
    "gluten", "crustáceos", "huevos", "pescado", "cacahuetes",
    "soja", "lácteos", "frutos con cáscara", "apio", "mostaza",
    "sésamo", "sulfitos", "altramuces", "moluscos"
]

class ModificarMenuConAlergenos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modificar Menú con Alérgenos")
        self.resize(600, 600)

        self.layout = QVBoxLayout()
        self.form = QFormLayout()

        # Fecha del menú
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        self.layout.addWidget(QLabel("Fecha del menú"))
        self.layout.addWidget(self.fecha_edit)

        # Crear campos por tipo de plato
        self.platos = []
        for tipo, cantidad in [("primero", 3), ("segundo", 3), ("postre", 2)]:
            for i in range(cantidad):
                nombre = QLineEdit()
                alergenos = [QCheckBox(al) for al in ALERGENOS]
                alergenos_layout = QHBoxLayout()
                for cb in alergenos:
                    alergenos_layout.addWidget(cb)

                contenedor = QWidget()
                contenedor.setLayout(alergenos_layout)

                self.form.addRow(f"{tipo.capitalize()} {i+1}:", nombre)
                self.form.addRow("Alérgenos:", contenedor)

                self.platos.append((nombre, tipo, alergenos))

        self.btn_guardar = QPushButton("Guardar menú")
        self.btn_guardar.clicked.connect(self.guardar_menu)

        self.layout.addLayout(self.form)
        self.layout.addWidget(self.btn_guardar)
        self.setLayout(self.layout)

    def guardar_menu(self):
        fecha = self.fecha_edit.date().toString("yyyy-MM-dd")
        dao = MenuDao()
        datos = []

        for nombre_edit, tipo, checkboxes in self.platos:
            nombre = nombre_edit.text().strip()
            if not nombre:
                continue
            alergenos = [cb.text() for cb in checkboxes if cb.isChecked()]
            datos.append((nombre, tipo, ",".join(alergenos)))

        if not datos:
            QMessageBox.warning(self, "Error", "Introduce al menos un plato.")
            return

        exito = dao.guardar_menu_con_alergenos(fecha, datos)

        if exito:
            QMessageBox.information(self, "Éxito", "Menú guardado con éxito.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar el menú.")
