from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from src.controlador.ControladorIngredientes import ControladorIngredientes

class StockComedor(QWidget):
    def __init__(self):
        super().__init__()
        # tu código aquí
        """
        self.setWindowTitle("Stock de Ingredientes")

        self.controlador = ControladorIngredientes()
        self.layout = QVBoxLayout()
        self.tabla = QTableWidget()
        self.boton_guardar = QPushButton("Guardar Cambios")

        self.layout.addWidget(self.tabla)
        self.layout.addWidget(self.boton_guardar)
        self.setLayout(self.layout)

        self.boton_guardar.clicked.connect(self.guardar_cambios)
        self.cargar_datos()
        """
        self.setWindowTitle("Stock de Ingredientes")

        self.controlador = ControladorIngredientes()
        self.layout = QVBoxLayout()
        self.tabla = QTableWidget()
        self.boton_aniadir = QPushButton("Añadir Stock")
        self.boton_guardar = QPushButton("Guardar Cambios")  # Nuevo botón

        self.layout.addWidget(self.tabla)
        self.layout.addWidget(self.boton_aniadir)
        self.layout.addWidget(self.boton_guardar)  # Añade el botón al layout
        self.setLayout(self.layout)

        self.filas_nuevas = set()

        self.boton_aniadir.clicked.connect(self.aniadir_fila)
        self.boton_guardar.clicked.connect(self.guardar_cambios)  # Conecta el botón
        self.tabla.cellChanged.connect(self.guardar_si_nueva_fila)

        self.cargar_datos()

    
    def cargar_datos(self):
        ingredientes = self.controlador.obtener_ingredientes()
        print("DEBUG ingredientes:", ingredientes)
        self.tabla.setRowCount(len(ingredientes))
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Unidad Medida", "Stock Actual", "Stock Mínimo", "Alergeno", "Tipo de Alergeno"
        ])

        for fila, ingrediente in enumerate(ingredientes):
            for col, valor in enumerate(ingrediente):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(valor)))

        self.tabla.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)

    def aniadir_fila(self):
        fila_actual = self.tabla.rowCount()
        self.tabla.insertRow(fila_actual)
        for col in range(self.tabla.columnCount()):
            self.tabla.setItem(fila_actual, col, QTableWidgetItem(""))
        self.filas_nuevas.add(fila_actual)


    def guardar_cambios(self):
        filas_actualizadas = 0
        filas_nuevas = 0
        for fila in range(self.tabla.rowCount()):
            datos = []
            for col in range(self.tabla.columnCount()):
                item = self.tabla.item(fila, col)
                datos.append(item.text() if item else "")
            try:
                id_ingrediente = datos[0]
                nombre = datos[1]
                unidad_medida = datos[2]
                stock_actual = float(datos[3]) if datos[3] else 0.0
                stock_minimo = float(datos[4]) if datos[4] else 0.0
                alergeno = datos[5].lower() in ("true", "1", "sí", "si")
                tipo_alergeno = datos[6]

                if id_ingrediente and id_ingrediente.isdigit():
                    # Actualizar ingrediente existente (ahora con todos los campos)
                    self.controlador.actualizar_ingrediente(
                        int(id_ingrediente), nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
                    )
                    filas_actualizadas += 1
                else:
                    # Guardar nuevo ingrediente
                    self.controlador.guardar_nuevo_ingrediente(
                        None, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
                    )
                    filas_nuevas += 1
            except Exception as e:
                print("Error al guardar el ingrediente:", e)
        QMessageBox.information(
            self,
            "Guardar Cambios",
            f"Se actualizaron {filas_actualizadas} ingredientes y se añadieron {filas_nuevas} nuevos."
        )
        self.cargar_datos()  # Refresca la tabla tras guardar
    
    def guardar_si_nueva_fila(self, row, column):
        if row in self.filas_nuevas:
            datos = []
            for col in range(self.tabla.columnCount()):
                item = self.tabla.item(row, col)
                datos.append(item.text() if item else "")
            try:
                nombre = datos[1]
                unidad_medida = datos[2]
                stock_actual = float(datos[3]) if datos[3] else 0.0
                stock_minimo = float(datos[4]) if datos[4] else 0.0
                alergeno = datos[5].lower() in ("true", "1", "sí", "si")
                tipo_alergeno = datos[6]
                # Guardar nuevo ingrediente (ID será None para autoincremental)
                self.controlador.guardar_nuevo_ingrediente(
                    None, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
                )
                self.filas_nuevas.remove(row)
                QMessageBox.information(self, "Nuevo ingrediente", "Ingrediente añadido correctamente.")
                self.cargar_datos()
            except Exception as e:
                print("Error al guardar el nuevo ingrediente:", e)
    
