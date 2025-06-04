from PyQt5.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QPushButton, QMessageBox
from src.vista.comun.GenerarTicket import GenerarTicket
from PyQt5 import uic
from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.UserVo import UserVo
from src.modelo.dao.PagoDao import PagoDao

Form, Window = uic.loadUiType("src/vista/ui/PagoWindow.ui")

class PagoWindow(QWidget, Form):
    def __init__(self, usuario, precio, metodo, callback_pago_exitoso, id_reserva):
        super().__init__()
        self.usuario = usuario
        self.precio = precio
        self.metodo = metodo
        self.callback_pago_exitoso = callback_pago_exitoso
        self.pago_realizado = False
        self.id_reserva = id_reserva  # <--- GUARDA EL ID DE RESERVA
        self.setupUi(self)
        self.setWindowTitle("Pago")

        # Detectar tipo
        tipo = usuario.rol  # 'estudiante', 'profesor', 'visitante'
        if tipo == 'estudiante':
            self.precio = 5.5
            self.metodo = 'tui'
        elif tipo == 'profesor':
            self.precio = 6.5
            self.metodo = 'tui'
        else:
            self.precio = 7.5
            self.metodo = 'tarjeta'

        self.labelPrecio.setText(f"Total: {self.precio:.2f} EUR")

        if self.metodo == 'tui':
            self.stackTarjeta.setVisible(False)
            self.btnPagar.clicked.connect(self.pagar_con_tui)
        else:
            self.stackTarjeta.setVisible(True)
            self.btnPagar.clicked.connect(self.pagar_con_tarjeta)

    def pagar_con_tui(self):
        saldo = self.usuario.saldo
        if saldo >= self.precio:
            nuevo_saldo = saldo - self.precio
            actualizado = BussinessObject().actualizarSaldo(self.usuario.idUser, nuevo_saldo)
            if actualizado:
                # Registrar el pago en la base de datos
                pago_dao = PagoDao()
                # Usa el id de reserva real
                pago_dao.insertar_pago(self.usuario.idUser, self.precio, "TUI", id_reserva=self.id_reserva)
                self.pago_realizado = True
                QMessageBox.information(self, "Éxito", "Pago con TUI realizado.")
                if self.callback_pago_exitoso:
                    self.callback_pago_exitoso()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el saldo.")
        else:
            QMessageBox.warning(self, "Saldo insuficiente", "No tienes saldo suficiente en el TUI.")

    def pagar_con_tarjeta(self):
        numero = self.inputNumero.text()
        fecha = self.inputCaducidad.text()
        cvv = self.inputCVV.text()

        if not (numero and fecha and cvv):
            QMessageBox.warning(self, "Campos vacíos", "Debes completar todos los campos.")
            return

        # Registrar el pago en la base de datos
        pago_dao = PagoDao()
        # Usa el id de reserva real
        pago_dao.insertar_pago(self.usuario.idUser, self.precio, "Tarjeta", id_reserva=self.id_reserva)

        self.pago_realizado = True
        QMessageBox.information(self, "Éxito", "Pago con tarjeta registrado.")
        if self.callback_pago_exitoso:
            self.callback_pago_exitoso()
        self.close()

    def closeEvent(self, event):
        print("Cerrando ventana de pago (evento closeEvent)")
        if not self.pago_realizado:
            print("Pago NO realizado")
        self.hide()  # Oculta la ventana en lugar de cerrarla
        event.ignore()  # Ignora el evento de cierre