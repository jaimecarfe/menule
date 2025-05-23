from PyQt5.QtWidgets import QApplication
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.modelo.BussinessObject import BussinessObject
from src.controlador.ControladorPrincipal import ControladorPrincipal

class App:
    def __init__(self):
        self.app = QApplication([])
        self.modelo = BussinessObject()
        self.login_window = Login()
        self.controlador = ControladorPrincipal(self.login_window, self.modelo)
        self.login_window.controlador = self.controlador
        self.login_window.abrir_registro = self.abrir_registro

    def abrir_registro(self):
        self.login_window.hide()
        self.registro_window = Registro()
        self.registro_window.controlador = self.controlador
        self.registro_window.show()

    def run(self):
        self.login_window.show()
        self.app.exec()

if __name__ == "__main__":
    app = App()
    app.run()
