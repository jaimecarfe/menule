from PyQt5.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QPushButton, QMessageBox
from src.vista.comun.GenerarTicket import GenerarTicket
from PyQt5 import uic
from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.UserVo import UserVo

Form, Window = uic.loadUiType("src/vista/ui/PagoWindow.ui")

class PagoWindow(QWidget, Form):
    def __init__(self, usuario, precio, metodo, callback_pago_exitoso):
        super().__init__()
        #self.id_reserva = id_reserva
        self.usuario = usuario
        self.precio = precio
        self.metodo = metodo
        self.callback_pago_exitoso = callback_pago_exitoso
        self.pago_realizado = False 
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

        self.labelPrecio.setText(f"Total: {self.precio:.2f} €")

        if self.metodo == 'tui':
            self.stackTarjeta.setVisible(False)
            self.btnPagar.clicked.connect(self.pagar_con_tui)
        else:
            self.stackTarjeta.setVisible(True)
            self.btnPagar.clicked.connect(self.pagar_con_tarjeta)

        '''
        layout = QVBoxLayout()
        self.radio_efectivo = QRadioButton("Efectivo")
        self.radio_tarjeta = QRadioButton("Tarjeta")
        self.btn_pagar = QPushButton("Pagar")
        self.btn_pagar.clicked.connect(self.confirmar_pago)

        layout.addWidget(self.radio_efectivo)
        layout.addWidget(self.radio_tarjeta)
        layout.addWidget(self.btn_pagar)
        self.setLayout(layout)
        '''

    def confirmar_pago(self):
        if not self.radio_efectivo.isChecked() and not self.radio_tarjeta.isChecked():
            QMessageBox.warning(self, "Selecciona un método", "Debes seleccionar un método de pago.")
            return

        metodo = "efectivo" if self.radio_efectivo.isChecked() else "tarjeta"
        QMessageBox.information(self, "Pago realizado", f"Pagado con {metodo}. Enviando ticket...")

        self.ticket = GenerarTicket(self.id_reserva)
        if hasattr(self.ticket, "enviar_ticket_por_correo_manual"):
            self.ticket.enviar_ticket_por_correo_manual(self.correo)
        self.ticket.show()
        self.close()


    def pagar_con_tui(self):
        saldo = self.usuario.saldo
        if saldo >= self.precio:
            nuevo_saldo = saldo - self.precio
            actualizado = BussinessObject().actualizarSaldo(self.usuario.idUser, nuevo_saldo)
            if actualizado:
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

        self.pago_realizado = True
        # Aquí podrías validar la tarjeta si lo deseas
        QMessageBox.information(self, "Éxito", "Pago con tarjeta registrado.")
        if self.callback_pago_exitoso:
                self.callback_pago_exitoso()
        self.close()

    def closeEvent(self, event):
        print("Cerrando ventana de pago (evento closeEvent)")
        if not self.pago_realizado:
            print("Pago NO realizado")
        event.accept()


