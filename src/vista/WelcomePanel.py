from PyQt5.QtWidgets import QMessageBox
from src.vista.VentanaBase import VentanaBase
from PyQt5 import uic
from src.vista.Login import Login

Form, Window = uic.loadUiType("./src/vista/ui/WelcomePanel.ui")

class WelcomePanel(VentanaBase, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(432, 505)