from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.vista.comun.PagoWindow import PagoWindow

class SeleccionarMenu(QWidget):
    def __init__(self, usuario, fecha, id_menu):
        super().__init__()
        self.usuario = usuario
        self.fecha = fecha
        self.id_menu = id_menu
        self.controlador = ControladorEstudiante()

        self.setWindowTitle(f"Seleccionar Menú para {fecha}")
        self.setGeometry(300, 300, 500, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Selecciona los platos:")
        layout.addWidget(self.label)

        self.listaPrimeros = QListWidget()
        self.listaSegundos = QListWidget()
        self.listaPostres = QListWidget()

        layout.addWidget(QLabel("Primer Plato"))
        layout.addWidget(self.listaPrimeros)
        layout.addWidget(QLabel("Segundo Plato"))
        layout.addWidget(self.listaSegundos)
        layout.addWidget(QLabel("Postre"))
        layout.addWidget(self.listaPostres)

        self.btnReservar = QPushButton("Reservar")
        self.btnReservar.clicked.connect(self.reservar)
        layout.addWidget(self.btnReservar)

        self.setLayout(layout)
        self.cargar_platos()

    def cargar_platos(self):
        platos = self.controlador.obtener_platos_por_fecha(self.fecha)
        for nombre, tipo, _ in platos:
            if tipo == "primero":
                self.listaPrimeros.addItem(nombre)
            elif tipo == "segundo":
                self.listaSegundos.addItem(nombre)
            elif tipo == "postre":
                self.listaPostres.addItem(nombre)

    def reservar(self):
        def get_text(list_widget):
            item = list_widget.currentItem()
            return item.text() if item else None

        primero = get_text(self.listaPrimeros)
        segundo = get_text(self.listaSegundos)
        postre = get_text(self.listaPostres)

        if not all([primero, segundo, postre]):
            QMessageBox.warning(self, "Error", "Debes seleccionar un plato de cada tipo.")
            return

        id_reserva = self.controlador.reservar_menu(
            self.usuario.idUser,
            self.id_menu,
            primero,
            segundo,
            postre
        )

        if id_reserva:
            self.abrir_pago(id_reserva)
        else:
            QMessageBox.critical(self, "Error", "No se pudo completar la reserva.")

    def abrir_pago(self, id_reserva):
        self.pago_window = PagoWindow(
            usuario=self.usuario,
            precio=3.5,  # o calcular dinámicamente según rol
            metodo_pago="tui",
            callback_pago_exitoso=None,
            id_reserva=id_reserva
        )
        self.pago_window.show()
