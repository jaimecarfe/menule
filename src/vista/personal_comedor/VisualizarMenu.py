from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorComedor import ControladorComedor
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/MenuComedor.ui")

class VisualizarMenu(VentanaBase, Form):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self.panel_anterior = parent
        self._controlador = ControladorComedor(self.usuario)
        self.setupUi(self)
        self.showFullScreen()
        self.configurar_interfaz()
        self.callback_cerrar_sesion = None

    def configurar_interfaz(self):
        self.setWindowTitle("Visualizar Menú")
        self.labelUsuario.setText(f"¿Qué tenemos que preparar hoy, {self.usuario.nombre}?")
        self.configurar_calendario()

        self.btnVolver.clicked.connect(self.volver_al_panel)
        self.btnVisualizarMenu.clicked.connect(self.ver_menu)

        self.setStyleSheet("""
            QListWidget, QLabel {
                color: white;
                font-size: 16px;
            }
        """)

    def validar_fecha_seleccionada(self):
        fecha = self.calendarWidget.selectedDate()
        if fecha.dayOfWeek() in (Qt.Saturday, Qt.Sunday):
            QMessageBox.warning(self, "Fecha inválida", "Selecciona un día entre lunes y viernes.")
            self.calendarWidget.setSelectedDate(QDate())
            self.btnVisualizarMenu.setEnabled(False)
        else:
            self.btnVisualizarMenu.setEnabled(True)

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

    def cargar_menu_del_dia(self):
        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        platos = self._controlador.obtener_platos_por_fecha(fecha)

        self.listaPrimeros.clear()
        self.listaSegundos.clear()
        self.listaPostres.clear()

        for nombre, tipo, alergenos in platos:
            texto = f"{nombre}  ({alergenos})" if alergenos else nombre
            if tipo == 'primero':
                self.listaPrimeros.addItem(texto)
            elif tipo == 'segundo':
                self.listaSegundos.addItem(texto)
            elif tipo == 'postre':
                self.listaPostres.addItem(texto)

    def ver_menu(self):
        if not self.calendarWidget.selectedDate().isValid():
            QMessageBox.warning(self, "Fecha inválida", "Selecciona una fecha válida en el calendario.")
            return

        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        if fecha < QDate.currentDate().toString("yyyy-MM-dd"):
            QMessageBox.warning(self, "Fecha inválida", "El menú de ese día no está disponible.")
            return

        self.cargar_menu_del_dia()

    def volver_al_panel(self):
        if self.parent():
            self.parent().showFullScreen()
        self.close()