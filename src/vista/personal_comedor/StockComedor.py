from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
from src.controlador.ControladorIngredientes import ControladorIngredientes

class StockComedor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock de Ingredientes")

        # Inicialización de componentes
        self.controlador = ControladorIngredientes()
        self.layout = QVBoxLayout()
        self.tabla = QTableWidget()
        self.boton_aniadir = QPushButton("Añadir Stock")
        self.boton_guardar = QPushButton("Guardar Cambios")

        # Añadir botones al layout
        self.layout.addWidget(self.tabla)
        self.layout.addWidget(self.boton_aniadir)
        self.layout.addWidget(self.boton_guardar)
        self.setLayout(self.layout)

        # alamacenamiento de datos originales
        self.filas_nuevas = set()

        # asignación de eventos a los botones
        self.boton_aniadir.clicked.connect(self.aniadir_fila)
        self.boton_guardar.clicked.connect(self.guardar_cambios)

        self.cargar_datos()

    
    def cargar_datos(self):
        """Carga los datos de los ingredientes en la tabla."""
        ingredientes = self.controlador.obtener_ingredientes()
        self.datos_originales = {}
        self.tabla.setRowCount(len(ingredientes))
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Unidad Medida", "Stock Actual", "Stock Mínimo", "Alergeno", "Tipo de Alergeno"
        ])

        for fila, ingrediente in enumerate(ingredientes):
            for col, valor in enumerate(ingrediente):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(valor)))
            # Guarda los datos originales usando el ID como clave
            self.datos_originales[str(ingrediente[0])] = tuple(str(v) for v in ingrediente)

        self.tabla.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)

    def aniadir_fila(self):
        """Añade una nueva fila vacía a la tabla."""
        fila_actual = self.tabla.rowCount()
        self.tabla.insertRow(fila_actual)
        for col in range(self.tabla.columnCount()):
            self.tabla.setItem(fila_actual, col, QTableWidgetItem(""))
        self.filas_nuevas.add(fila_actual)


    def guardar_cambios(self):
        """Guarda los cambios realizados en la tabla almacenandolos a la base de datos"""
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
                    if fila in self.filas_nuevas:
                        self.controlador.guardar_nuevo_ingrediente(
                            int(id_ingrediente), nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
                        )
                        filas_nuevas += 1
                    else:
                        # Compara con los datos originales
                        original = self.datos_originales.get(id_ingrediente)
                        actual = (
                            id_ingrediente,
                            nombre,
                            unidad_medida,
                            str(stock_actual),
                            str(stock_minimo),
                            str(alergeno),
                            tipo_alergeno
                        )
                        if original and actual != original:
                            self.controlador.actualizar_ingrediente(
                                int(id_ingrediente), nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
                            )
                            filas_actualizadas += 1
                elif fila in self.filas_nuevas:
                    self.controlador.guardar_nuevo_ingrediente(
                        None, nombre, unidad_medida, stock_actual, stock_minimo, alergeno, tipo_alergeno
                    )
                    filas_nuevas += 1
            except Exception as e:
                print("Error al guardar el ingrediente:", e)
        self.filas_nuevas.clear()
        QMessageBox.information(
            self,
            "Guardar Cambios",
            f"Se actualizaron {filas_actualizadas} ingredientes y se añadieron {filas_nuevas} nuevos."
        )
        self.cargar_datos()
