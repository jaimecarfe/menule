from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorProfesor import ControladorProfesor
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/MenuProfesor.ui")

class MenuProfesor(VentanaBase, Form):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self._controlador = ControladorProfesor()
        self._callback_cerrar_sesion = None
        self.configurar_interfaz()

    def configurar_interfaz(self):
        super().setupUi(self)
        self.menuTextEdit.setReadOnly(True)
        self.setWindowTitle("Menú Profesor")
        self.labelUsuario.setText(f"¿Qué habrá de comer hoy, {self.usuario.nombre}?")
        self.configurar_calendario()
        self.btnVisualizarMenu.setEnabled(False)
        self.btnVisualizarMenu.clicked.connect(self.visualizar_menu)
        self.btnVolver.clicked.connect(self.volver_al_panel)

        self.setStyleSheet("""
            QListWidget {
                background-color: #e3f2fd;
                color: black;
                font-size: 16px;
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)

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
        elif fecha < QDate.currentDate():
            QMessageBox.warning(self, "Fecha inválida", "El menú de ese día no está disponible.")
            self.calendarWidget.setSelectedDate(QDate())
            self.btnVisualizarMenu.setEnabled(False)
        else:
            self.btnVisualizarMenu.setEnabled(True)

    def visualizar_menu(self):
        fecha = self.calendarWidget.selectedDate()
        if fecha.isValid():
            fecha_str = fecha.toString("yyyy-MM-dd")
            platos = self._controlador.obtener_menu_por_fecha(fecha_str)
            texto_menu = self.formatear_menu(platos, fecha)
            self.menuTextEdit.setText(texto_menu)
        else:
            QMessageBox.information(self, "Sin fecha", "Por favor selecciona un día válido.")

    def formatear_menu(self, platos, fecha_qdate):
        primeros = [p[0] for p in platos if p[1] == "primero"]
        segundos = [p[0] for p in platos if p[1] == "segundo"]
        postres = [p[0] for p in platos if p[1] == "postre"]

        texto_fecha = fecha_qdate.toString("dddd dd/MM/yyyy")
        return (
            f"Menú para el {texto_fecha}:\n\n"
            f"Primeros:\n- " + "\n- ".join(primeros or ["(No disponible)"]) + "\n\n"
            f"Segundos:\n- " + "\n- ".join(segundos or ["(No disponible)"]) + "\n\n"
            f"Postres:\n- " + "\n- ".join(postres or ["(No disponible)"])
        )

    def volver_al_panel(self):
        if self.parent():
            self.parent().show()
        self.close()
