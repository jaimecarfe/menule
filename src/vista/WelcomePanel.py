from PyQt5.QtWidgets import QMessageBox
from src.vista.VentanaBase import VentanaBase
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

Form, Window = uic.loadUiType("./src/vista/ui/WelcomePanel.ui")

class WelcomePanel(VentanaBase, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(432, 505)
        logo_path = "./src/vista/imagenes/paneles.png"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            self.labelImagen.setPixmap(pixmap.scaled(
                self.labelImagen.width(),
                self.labelImagen.height(),
                aspectRatioMode=Qt.KeepAspectRatio,
                transformMode=Qt.SmoothTransformation
            ))
            self.labelImagen.setStyleSheet("background: transparent;")
        else:
            self.labelImagen.setText("")