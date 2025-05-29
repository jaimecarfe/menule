from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorEstudiante import ControladorEstudiante
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/MenuEstudiante.ui")

class MenuEstudiante(VentanaBase, Form):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.configurar_interfaz()
        self._controlador = ControladorEstudiante(self.usuario)

        self._callback_cerrar_sesion = None

    def configurar_interfaz(self):
        super().setupUi(self)
        self.menuTextEdit.setReadOnly(True)
        self.setWindowTitle("Menú Estudiante")
        self.labelUsuario.setText(f"Bienvenido, {self.usuario.nombre}")
        self.configurar_calendario()
        self.btnVisualizarMenu.setEnabled(False)
        self.btnVisualizarMenu.clicked.connect(self.visualizar_menu)
        self.btnVolver.clicked.connect(self.volver_al_panel)


    def configurar_calendario(self):
        # Definir fechas del curso 2024–2025
        fecha_inicio = QDate(2024, 9, 6)
        fecha_fin = QDate(2025, 6, 23)

        self.calendarWidget.setMinimumDate(fecha_inicio)
        self.calendarWidget.setMaximumDate(fecha_fin)

        # Deshabilitar visualmente sábados y domingos
        formato_inhabilitado = QTextCharFormat()
        formato_inhabilitado.setForeground(QColor('gray'))
        formato_inhabilitado.setBackground(QColor('#f0f0f0'))

        fecha = fecha_inicio
        while fecha <= fecha_fin:
            if fecha.dayOfWeek() in (Qt.Saturday, Qt.Sunday):
                self.calendarWidget.setDateTextFormat(fecha, formato_inhabilitado)
            fecha = fecha.addDays(1)

        # Conectar evento para validar selección
        self.calendarWidget.selectionChanged.connect(self.validar_fecha_seleccionada)

    def validar_fecha_seleccionada(self):
        fecha = self.calendarWidget.selectedDate()
        if fecha.dayOfWeek() in (Qt.Saturday, Qt.Sunday):
            QMessageBox.warning(self, "Fecha inválida", "Selecciona un día entre lunes y viernes.")
            self.calendarWidget.setSelectedDate(QDate())
        else:
            self.btnVisualizarMenu.setEnabled(True)

    def visualizar_menu(self):
        fecha = self.calendarWidget.selectedDate()
        if fecha.isValid():
            texto_fecha = fecha.toString("dddd dd/MM/yyyy")
            # Aquí puedes conectar con la lógica del controlador para obtener el menú del día
            self.menuTextEdit.setText(f"Menú para el {texto_fecha}:\n\n- Primer plato\n- Segundo plato\n- Postre")
        else:
            QMessageBox.information(self, "Sin fecha", "Por favor selecciona un día válido.")

    def volver_al_panel(self):
        self.close()
