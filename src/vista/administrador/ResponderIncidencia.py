from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PyQt5 import uic
from datetime import date
from PyQt5.QtCore import Qt
from src.controlador.ControladorAdmin import ControladorAdmin

Form, Window = uic.loadUiType("./src/vista/ui/ResponderIncidencia.ui")
class ResponderIncidenciaWindow(QWidget, Form):
    def __init__(self, id_incidencia, titulo, descripcion, callback_guardado):
        super().__init__()
        self.setupUi(self)
        self.id_incidencia = id_incidencia
        self.callback_guardado = callback_guardado

        self.controlador = ControladorAdmin()

        self.tituloLabel.setText(titulo)
        self.descripcionLabel.setText(descripcion)

        self.enviarBtn.clicked.connect(self.enviar_respuesta)

    def enviar_respuesta(self):
        respuesta = self.respuestaBox.toPlainText().strip()
        if not respuesta:
            QMessageBox.warning(self, "Error", "La respuesta no puede estar vacía.")
            return

        self.controlador.responder_incidencia(self.id_incidencia, respuesta, date.today())

        QMessageBox.information(self, "Éxito", "Respuesta guardada y enviada.")
        if self.callback_guardado:
            self.callback_guardado()
        self.close()
