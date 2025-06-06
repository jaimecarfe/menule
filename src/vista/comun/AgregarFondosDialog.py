from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic

class AgregarFondosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("src/vista/ui/agregarfondos.ui", self)

        self.btn_agregar.clicked.connect(self.validar)
        self.btn_cancelar.clicked.connect(self.reject)

        self.cantidad = 0.0

    def validar(self):
        try:
            cantidad = float(self.input_cantidad.text())
            if cantidad <= 0:
                raise ValueError
            self.cantidad = cantidad
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "Introduce una cantidad positiva válida.")
