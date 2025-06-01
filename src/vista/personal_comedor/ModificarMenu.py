from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QDateEdit, QLineEdit,
    QPushButton, QMessageBox, QFormLayout
)
from PyQt5.QtCore import QDate
from src.modelo.dao.MenuDao import MenuDao

class ModificarMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modificar Menú del Día")
        self.resize(400, 400)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.fecha_label = QLabel("Selecciona una fecha:")
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)

        layout.addWidget(self.fecha_label)
        layout.addWidget(self.fecha_edit)

        # Primeros platos
        self.primero1 = QLineEdit()
        self.primero2 = QLineEdit()
        self.primero3 = QLineEdit()
        form.addRow("Primer Plato 1:", self.primero1)
        form.addRow("Primer Plato 2:", self.primero2)
        form.addRow("Primer Plato 3:", self.primero3)

        # Segundos platos
        self.segundo1 = QLineEdit()
        self.segundo2 = QLineEdit()
        self.segundo3 = QLineEdit()
        form.addRow("Segundo Plato 1:", self.segundo1)
        form.addRow("Segundo Plato 2:", self.segundo2)
        form.addRow("Segundo Plato 3:", self.segundo3)

        # Postres
        self.postre1 = QLineEdit()
        self.postre2 = QLineEdit()
        form.addRow("Postre 1:", self.postre1)
        form.addRow("Postre 2:", self.postre2)

        layout.addLayout(form)

        self.btn_guardar = QPushButton("Guardar menú")
        self.btn_guardar.clicked.connect(self.guardar_menu)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_menu(self):
        fecha = self.fecha_edit.date().toString("yyyy-MM-dd")

        platos = []
        for tipo, campos in [
            ("primero", [self.primero1, self.primero2, self.primero3]),
            ("segundo", [self.segundo1, self.segundo2, self.segundo3]),
            ("postre",  [self.postre1, self.postre2])
        ]:
            for campo in campos:
                nombre = campo.text().strip()
                if nombre:
                    platos.append((nombre, tipo))

        if len(platos) < 3:
            QMessageBox.warning(self, "Error", "Debes introducir al menos un plato de cada tipo.")
            return

        dao = MenuDao()
        exito = dao.insertar_o_modificar_menu_con_tipo(fecha, platos)

        if exito:
            QMessageBox.information(self, "Éxito", f"Menú guardado para {fecha}")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Hubo un problema al guardar el menú.")
