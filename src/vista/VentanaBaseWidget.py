from PyQt5.QtWidgets import QWidget
from src.vista.VentanaBase import VentanaBase

class VentanaBaseWidget(QWidget, VentanaBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        VentanaBase.__init__(self, parent)