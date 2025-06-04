from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from src.modelo.dao.ReservaDao import ReservaDao
from src.vista.comun.PagoWindow import PagoWindow

class SeleccionarMenu(QWidget):
    def __init__(self, usuario, id_menu, platos_menu):
        super().__init__()
        self.usuario = usuario
        self.id_menu = id_menu
        self.platos_menu = platos_menu

        self.setWindowTitle("Selecciona tu menú")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Primer Plato:"))
        self.combo_primero = QComboBox()
        layout.addWidget(self.combo_primero)

        layout.addWidget(QLabel("Segundo Plato:"))
        self.combo_segundo = QComboBox()
        layout.addWidget(self.combo_segundo)

        layout.addWidget(QLabel("Postre o Fruta:"))
        self.combo_postre = QComboBox()
        layout.addWidget(self.combo_postre)

        self.btn_reservar = QPushButton("Reservar y Pagar")
        self.btn_reservar.clicked.connect(self.reservar)
        layout.addWidget(self.btn_reservar)

        self.setLayout(layout)
        self.cargar_platos()

    def cargar_platos(self):
        primeros = [p['nombre'] for p in self.platos_menu if p['tipo'] == 'primero']
        segundos = [p['nombre'] for p in self.platos_menu if p['tipo'] == 'segundo']
        postres = [p['nombre'] for p in self.platos_menu if p['tipo'] == 'postre']

        self.combo_primero.addItems(primeros)
        self.combo_segundo.addItems(segundos)
        self.combo_postre.addItems(postres)

    def reservar(self):
        primero = self.combo_primero.currentText()
        segundo = self.combo_segundo.currentText()
        postre = self.combo_postre.currentText()

        if not (primero and segundo and postre):
            QMessageBox.warning(self, "Incompleto", "Debes seleccionar un plato de cada categoría.")
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar selección",
            f"¿Seguro que quieres seleccionar este menú?\n\n{primero}\n{segundo}\n{postre}",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            # Insertar reserva
            dao = ReservaDao()
            id_reserva = dao.crear_reserva_completa(self.usuario.idUser, self.id_menu, primero, segundo, postre)

            if id_reserva:
                # Mostrar pantalla de pago
                self.pago = PagoWindow(id_reserva, self.usuario)
                self.pago.show()
                self.close()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la reserva.")
