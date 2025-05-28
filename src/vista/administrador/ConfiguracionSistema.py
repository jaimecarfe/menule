from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class ConfiguracionSistema(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.setWindowTitle("Configuración del Sistema")
        self.layout = QVBoxLayout()

        self.tiempoReserva = QLineEdit()
        self.tiempoReserva.setPlaceholderText("Tiempo máximo de reserva (minutos)")
        self.layout.addWidget(QLabel("Tiempo de reserva"))
        self.layout.addWidget(self.tiempoReserva)

        self.botonGuardar = QPushButton("Guardar")
        self.botonGuardar.clicked.connect(self.guardar_configuracion)
        self.layout.addWidget(self.botonGuardar)

        self.setLayout(self.layout)
        self.cargar_configuracion()

    def cargar_configuracion(self):
        conf = self.controlador.obtener_configuraciones()
        self.tiempoReserva.setText(conf.get("tiempo_reserva", ""))

    def guardar_configuracion(self):
        valor = self.tiempoReserva.text()
        if self.controlador.guardar_configuracion("tiempo_reserva", valor):
            QMessageBox.information(self, "Éxito", "Configuración guardada.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la configuración.")
