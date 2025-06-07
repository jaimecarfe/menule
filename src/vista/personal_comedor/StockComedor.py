from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
from src.controlador.ControladorIngredientes import ControladorIngredientes

class StockComedor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Stock de Ingredientes")
        self.setGeometry(200, 200, 900, 400)
        self.controlador = ControladorIngredientes()

        layout = QVBoxLayout()
        self.tabla = QTableWidget()
        layout.addWidget(QLabel("Ingredientes actuales:"))
        layout.addWidget(self.tabla)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.actualizar_stock)
        layout.addWidget(self.btn_actualizar)

        self.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos de los ingredientes en la tabla."""
        ingredientes = self.controlador.obtener_ingredientes()
        self.tabla.setRowCount(len(ingredientes))
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Unidad", "Stock", "Mínimo", "Alergeno", "Tipo Alergeno"])

        for i, ing in enumerate(ingredientes):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(ing["id"])))
            self.tabla.setItem(i, 1, QTableWidgetItem(ing["nombre"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(ing["unidad"]))
            self.tabla.setItem(i, 3, QTableWidgetItem(str(ing["stock"])))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(ing["minimo"])))
            self.tabla.setItem(i, 5, QTableWidgetItem(str(ing["alergeno"])))
            self.tabla.setItem(i, 6, QTableWidgetItem(ing["tipo"] or ""))

    def actualizar_stock(self):
        filas = self.tabla.rowCount()
        for i in range(filas):
            try:
                id_ing = int(self.tabla.item(i, 0).text())
                nombre = self.tabla.item(i, 1).text()
                unidad = self.tabla.item(i, 2).text()
                stock = float(self.tabla.item(i, 3).text())
                minimo = float(self.tabla.item(i, 4).text())
                alergeno = self.tabla.item(i, 5).text()
                tipo = self.tabla.item(i, 6).text()
                self.controlador.actualizar_ingrediente(id_ing, nombre, unidad, stock, minimo, alergeno, tipo)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error en la fila {i+1}: {str(e)}")
                return
        QMessageBox.information(self, "Éxito", "Stock actualizado correctamente.")
