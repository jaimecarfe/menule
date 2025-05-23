from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
import os

class VentanaBase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.abspath("src/vista/logo/logo.png")))
