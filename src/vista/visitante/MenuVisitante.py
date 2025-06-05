from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorVisitante import ControladorVisitante
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/MenuVisitante.ui")

class MenuVisitante(VentanaBase, Form):
    def __init__(self):
        super().__init__()
        self.configurar_interfaz()
        self._controlador = ControladorVisitante()

        self._callback_cerrar_sesion = None

    def configurar_interfaz(self):
        super().setupUi(self)
        self.menuTextEdit.setReadOnly(True)
        self.setWindowTitle("Menú Visitante")
        self.labelUsuario.setText("¿Qué habrá de comer hoy?")
        self.configurar_calendario()
        self.btnVisualizarMenu.setEnabled(False)
        self.btnVisualizarMenu.clicked.connect(self.visualizar_menu)
        self.btnVolver.clicked.connect(self.volver_al_panel)

    def configurar_calendario(self):
        fecha_inicio = QDate(2024, 9, 6)
        fecha_fin = QDate(2025, 6, 23)
        fecha_actual = QDate.currentDate()

        self.calendarWidget.setMinimumDate(max(fecha_inicio, fecha_actual))
        self.calendarWidget.setMaximumDate(fecha_fin)

        formato_inhabilitado = QTextCharFormat()
        formato_inhabilitado.setForeground(QColor('gray'))
        formato_inhabilitado.setBackground(QColor('#f0f0f0'))

        fecha = max(fecha_inicio, fecha_actual)
        while fecha <= fecha_fin:
            if fecha.dayOfWeek() in (Qt.Saturday, Qt.Sunday):
                self.calendarWidget.setDateTextFormat(fecha, formato_inhabilitado)
            fecha = fecha.addDays(1)

        self.calendarWidget.selectionChanged.connect(self.validar_fecha_seleccionada)

    def validar_fecha_seleccionada(self):
        fecha = self.calendarWidget.selectedDate()
        if fecha.dayOfWeek() in (Qt.Saturday, Qt.Sunday):
            QMessageBox.warning(self, "Fecha inválida", "Selecciona un día entre lunes y viernes.")
            self.calendarWidget.setSelectedDate(QDate())
            self.btnVisualizarMenu.setEnabled(False)
            self.btnReservarComida.setVisible(False)
        elif fecha < QDate.currentDate():
            QMessageBox.warning(self, "Fecha inválida", "El menú de ese día no está disponible.")
            self.calendarWidget.setSelectedDate(QDate())
            self.btnVisualizarMenu.setEnabled(False)
            self.btnReservarComida.setVisible(False)
        else:
            self.btnVisualizarMenu.setEnabled(True)

    def visualizar_menu(self):
        fecha = self.calendarWidget.selectedDate()

    def volver_al_panel(self):
        respuesta = QMessageBox.question(
            self,
            "Confirmación",
            "¿Quieres volver al inicio?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            if self._callback_cerrar_sesion:
                self._callback_cerrar_sesion()
            else:
                from src.vista.Login import Login
                self.close()
                self.deleteLater()
                self._login = Login()
                self._login.showFullScreen()
            self.close()
