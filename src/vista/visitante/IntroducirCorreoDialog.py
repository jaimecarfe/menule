from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QVBoxLayout, QMessageBox

class IntroducirCorreoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QWidget {
            background-color: #e6f2ff;
            font-family: Arial;
            font-size: 14px;
        }
        QLabel {
            color: #005c99;
            font-weight: bold;
        }
        QLineEdit {
            border: 1px solid #80bfff;
            border-radius: 5px;
            padding: 5px;
            background-color: white;
        }
        QPushButton {
            background-color: #00cc99;
            color: white;
            border-radius: 10px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #009973;
        }
        """)
        
        self.setWindowTitle("Introduce tu correo")
        self.setModal(True)

        self.label = QLabel("Introduce tu correo electrónico para recibir el tíquet de reserva:")
        self.input = QLineEdit()
        self.input.setPlaceholderText("ejemplo@correo.com")
        self.btn_enviar = QPushButton("Enviar")
        self.btn_cancelar = QPushButton("Cancelar")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn_enviar)
        layout.addWidget(self.btn_cancelar)
        self.setLayout(layout)

        self.btn_enviar.clicked.connect(self.validar_y_aceptar)
        self.btn_cancelar.clicked.connect(self.reject)
        self.correo = None

    def validar_y_aceptar(self):
        correo = self.input.text().strip()
        if "@" in correo and "." in correo:
            self.correo = correo
            self.accept()
        else:
            QMessageBox.warning(self, "Correo inválido", "Introduce un correo electrónico válido.")