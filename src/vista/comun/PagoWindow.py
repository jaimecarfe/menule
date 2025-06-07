from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QLabel, QLineEdit, QPushButton
from PyQt5 import uic
from src.controlador.ControladorPagos import ControladorPagos

Form, Window = uic.loadUiType("src/vista/ui/PagoWindow.ui")

class PagoWindow(QWidget, Form):
    def __init__(self, usuario, precio, metodo, callback_pago_exitoso, id_reserva):
        super().__init__()
        self.usuario = usuario
        self.precio = precio
        self.metodo = metodo
        self.id_reserva = id_reserva
        self.callback_pago_exitoso = callback_pago_exitoso
        self.controlador = ControladorPagos()
        self.pago_realizado = False

        self.setupUi(self)

        self.setWindowTitle("Pago")
        self.labelPrecio.setText(f"Total: {self.precio:.2f} EUR")

        if self.metodo == 'tui':
            self.stackTarjeta.setVisible(False)
            self.btnPagar.clicked.connect(self.realizar_pago_tui)
        else:
            self.stackTarjeta.setVisible(True)
            self.btnPagar.clicked.connect(self.realizar_pago_tarjeta)

    def realizar_pago_tui(self):
        ok, mensaje = self.controlador.pagar_con_tui(self.usuario, self.precio, self.id_reserva)
        self._finalizar_pago(ok, mensaje)

    def realizar_pago_tarjeta(self):
        if self.usuario.rol == "visitante":
            numero = self.inputNumero.text().strip()
            fecha = self.inputCaducidad.text().strip()
            cvv = self.inputCVV.text().strip()

            if not all([numero, fecha, cvv]):
                QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
                return

            ok, mensaje = self.controlador.pagar_con_tarjeta(
                monto=self.precio,
                id_reserva=self.id_reserva,
                id_usuario=0  # visitante = usuario anónimo
            )
        else:
            ok, mensaje = self.controlador.pagar_con_tarjeta(
                correo=self.usuario.correo,
                monto=self.precio,
                id_reserva=self.id_reserva,
                id_usuario=self.usuario.idUser
            )

        self._finalizar_pago(ok, mensaje)

    def _finalizar_pago(self, ok, mensaje):
        if ok:
            QMessageBox.information(self, "Pago exitoso", mensaje)
            self.pago_realizado = True
            if self.callback_pago_exitoso:
                self.callback_pago_exitoso()
            self.close()
        else:
            QMessageBox.warning(self, "Error de pago", mensaje)

    def closeEvent(self, event):
        if not self.pago_realizado:
            print("Pago no completado")
        self.hide()
        event.ignore()

