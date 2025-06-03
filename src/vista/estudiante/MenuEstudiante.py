from PyQt5.QtWidgets import QMainWindow, QMessageBox, QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.vista.estudiante.ReservaComida import ReservaComida
from src.modelo.dao.MenuDao import MenuDao
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/ui/MenuEstudiante.ui")

class MenuEstudiante(VentanaBase, Form):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        self._controlador = ControladorEstudiante()
        self._callback_cerrar_sesion = None
        self.setupUi(self)
        self.init_layouts()
        self.configurar_interfaz()

    def init_layouts(self):
        # Creamos el layout principal si no existe
        self.layout_principal = QHBoxLayout()

        # Crear layout derecho para platos
        self.layout_derecho = QVBoxLayout()

        self.lista_primero = QListWidget()
        self.lista_segundo = QListWidget()
        self.lista_postre = QListWidget()

        self.layout_derecho.addWidget(QLabel("Primeros platos"))
        self.layout_derecho.addWidget(self.lista_primero)
        self.layout_derecho.addWidget(QLabel("Segundos platos"))
        self.layout_derecho.addWidget(self.lista_segundo)
        self.layout_derecho.addWidget(QLabel("Postres"))
        self.layout_derecho.addWidget(self.lista_postre)

        # Suponemos que ya hay un widget padre en el .ui como contenedor central
        self.menuContentWidget = QWidget()  # si no existe en .ui, lo creamos
        self.menuContentWidget.setLayout(self.layout_derecho)

        # Añadir ambos layouts (izquierda de QtDesigner + derecha dinámica)
        self.layout_principal.addLayout(self.mainVerticalLayout) # del .ui (calendario y botones)
        self.layout_principal.addWidget(self.menuContentWidget)

        self.setLayout(self.layout_principal)

    def configurar_interfaz(self):
        self.setWindowTitle("Menú Estudiante")
        self.labelUsuario.setText(f"¿Qué habrá de comer hoy, {self.usuario.nombre}?")
        self.configurar_calendario()

        self.btnVisualizarMenu.setEnabled(False)
        self.btnVisualizarMenu.clicked.connect(self.visualizar_menu)
        self.btnVolver.clicked.connect(self.volver_al_panel)
        self.btnReservarComida.setVisible(False)
        self.btnReservarComida.clicked.connect(self.confirmar_reserva)

        # Crear las listas dinámicamente dentro del contenedor ya definido en el .ui
        self.lista_primero = QListWidget()
        self.lista_segundo = QListWidget()
        self.lista_postre = QListWidget()

        layout_derecha = QVBoxLayout(self.contenedorMenuDerecha)
        layout_derecha.addWidget(QLabel("Primeros platos"))
        layout_derecha.addWidget(self.lista_primero)
        layout_derecha.addWidget(QLabel("Segundos platos"))
        layout_derecha.addWidget(self.lista_segundo)
        layout_derecha.addWidget(QLabel("Postres"))
        layout_derecha.addWidget(self.lista_postre)


    def configurar_calendario(self):
        fecha_inicio = QDate(2024, 9, 6)
        fecha_fin = QDate(2025, 6, 23)

        self.calendarWidget.setMinimumDate(fecha_inicio)
        self.calendarWidget.setMaximumDate(fecha_fin)

        formato_inhabilitado = QTextCharFormat()
        formato_inhabilitado.setForeground(QColor('gray'))
        formato_inhabilitado.setBackground(QColor('#f0f0f0'))

        fecha = fecha_inicio
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
        else:
            self.btnVisualizarMenu.setEnabled(True)

    def visualizar_menu(self):
        fecha = self.calendarWidget.selectedDate()
        if fecha.isValid():
            self.cargar_menu_del_dia()
            self.btnReservarComida.setVisible(True)
        else:
            QMessageBox.information(self, "Sin fecha", "Por favor selecciona un día válido.")
            self.btnReservarComida.setVisible(False)

    def cargar_menu_del_dia(self):
        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        dao = MenuDao()
        platos = dao.obtener_platos_por_fecha(fecha)

        self.lista_primero.clear()
        self.lista_segundo.clear()
        self.lista_postre.clear()

        for nombre, tipo in platos:
            if tipo == 'primero':
                self.lista_primero.addItem(nombre)
            elif tipo == 'segundo':
                self.lista_segundo.addItem(nombre)
            elif tipo == 'postre':
                self.lista_postre.addItem(nombre)

    def confirmar_reserva(self):
        respuesta = QMessageBox.question(
            self,
            "Confirmar reserva",
            "¿Quieres reservar este menú?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.abrir_reserva_comida()

    def abrir_reserva_comida(self):
        reserva_comida = ReservaComida(self.usuario, self)
        reserva_comida.show()

    def volver_al_panel(self):
        if self.parent():
            self.parent().show()
        self.close()
