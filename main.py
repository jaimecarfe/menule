from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from src.vista.Login import Login
from src.vista.Registro import Registro
from src.modelo.BussinessObject import BussinessObject
from src.controlador.ControladorPrincipal import ControladorPrincipal


if __name__ == "__main__":
    app = QApplication([])
    ventana = Login()
    modelo = BussinessObject()
    controlador = ControladorPrincipal(ventana, modelo)
    ventana.controlador = controlador

    ventana.show()
    app.exec()