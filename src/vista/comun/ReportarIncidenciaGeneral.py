from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import QDate
import uuid
from datetime import datetime
from src.modelo.vo.IncidenciaVo import IncidenciaVo
from src.modelo.Sesion import Sesion
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.controlador.ControladorProfesor import ControladorProfesor
from src.controlador.ControladorComedor import ControladorComedor

class ReportarIncidenciaGeneral(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/vista/ui/ReportarIncidencia.ui", self)

        # Establecer fecha actual y deshabilitar edición
        hoy = QDate.currentDate()
        self.fecha_input.setDate(hoy)
        self.fecha_input.setEnabled(False)

        self.enviar_btn.clicked.connect(self.enviar_incidencia)

    def enviar_incidencia(self):
        sesion = Sesion()
        correo = sesion.usuario.correo
        rol = sesion.usuario.rol
        titulo = self.titulo_input.text().strip()
        descripcion = self.descripcion_input.toPlainText().strip()

        # Validación de campos obligatorios
        if not titulo or not descripcion:
            QMessageBox.warning(self, "Campos obligatorios", "Por favor, completa el título y la descripción.")
            return

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        estado = "en_proceso"
        numero_seguimiento = str(uuid.uuid4())[:8]

        incidencia = IncidenciaVo(
            id=sesion.usuario.idUser,
            titulo=titulo,
            descripcion=descripcion,
            fecha=fecha,
            correo=correo,
            estado=estado,
            numero_seguimiento=numero_seguimiento
        )

        if rol == "estudiante":
            ControladorEstudiante().reportar_incidencia(incidencia)
        elif rol == "profesor":
            ControladorProfesor().reportar_incidencia(incidencia)
        elif rol == "personal_comedor":
            ControladorComedor().reportar_incidencia(incidencia)
        else:
            QMessageBox.critical(self, "Error", "Rol no autorizado para reportar incidencias.")
            return

        resumen = f"""
        Número de Seguimiento: {numero_seguimiento}
        Título: {titulo}
        Correo: {correo}
        Fecha: {fecha}
        Descripción: {descripcion}
        """
        QMessageBox.information(self, "Incidencia Reportada", resumen)
        self.close()
