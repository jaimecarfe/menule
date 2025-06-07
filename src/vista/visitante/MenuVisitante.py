from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorVisitante import ControladorVisitante
from PyQt5 import uic
from src.vista.comun.PagoWindow import PagoWindow
from src.modelo.vo.UserVo import UserVo
from src.vista.comun.GenerarTicket import GenerarTicket

Form, Window = uic.loadUiType("./src/vista/ui/MenuVisitante.ui")

def mostrar_warning(parent, titulo, mensaje):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle(titulo)
    msg.setText(mensaje)
    # Opción 1: Fondo oscuro elegante
    msg.setStyleSheet("""
        QMessageBox { background-color: #222; color: #fff; font-size: 16px; }
        QLabel { color: #fff; font-size: 16px; font-family: Arial, sans-serif; }
        QPushButton { background-color: #26a69a; color: white; font-weight: bold;
                      border-radius: 8px; min-width: 60px; padding: 8px 16px; }
        QPushButton:hover { background-color: #009973; }
    """)
    # Opción 2: Fondo claro (descomenta si lo prefieres)
    # msg.setStyleSheet("""
    #     QMessageBox { background-color: #e6f2ff; color: #005c99; font-size: 16px; }
    #     QLabel { color: #005c99; font-size: 16px; font-family: Arial, sans-serif; }
    #     QPushButton { background-color: #26a69a; color: white; font-weight: bold;
    #                   border-radius: 8px; min-width: 60px; padding: 8px 16px; }
    #     QPushButton:hover { background-color: #009973; }
    # """)
    msg.exec_()

def mostrar_info(parent, titulo, mensaje):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(titulo)
    msg.setText(mensaje)
    msg.setStyleSheet("""
        QMessageBox { background-color: #e6f2ff; color: #005c99; font-size: 16px; }
        QLabel { color: #005c99; font-size: 16px; font-family: Arial, sans-serif; }
        QPushButton { background-color: #26a69a; color: white; font-weight: bold;
                      border-radius: 8px; min-width: 60px; padding: 8px 16px; }
        QPushButton:hover { background-color: #009973; }
    """)
    msg.exec_()

def mostrar_error(parent, titulo, mensaje):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(titulo)
    msg.setText(mensaje)
    msg.setStyleSheet("""
        QMessageBox { background-color: #222; color: #fff; font-size: 16px; }
        QLabel { color: #fff; font-size: 16px; font-family: Arial, sans-serif; }
        QPushButton { background-color: #e53935; color: white; font-weight: bold;
                      border-radius: 8px; min-width: 60px; padding: 8px 16px; }
        QPushButton:hover { background-color: #b71c1c; }
    """)
    msg.exec_()

def mostrar_pregunta(parent, titulo, mensaje):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Question)
    msg.setWindowTitle(titulo)
    msg.setText(mensaje)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setStyleSheet("""
        QMessageBox { background-color: #e6f2ff; color: #005c99; font-size: 16px; }
        QLabel { color: #005c99; font-size: 16px; font-family: Arial, sans-serif; }
        QPushButton { background-color: #26a69a; color: white; font-weight: bold;
                      border-radius: 8px; min-width: 60px; padding: 8px 16px; }
        QPushButton:hover { background-color: #009973; }
    """)
    return msg.exec_()

class MenuVisitante(VentanaBase, Form):
    def __init__(self):
        super().__init__()
        self.configurar_interfaz()
        self._controlador = ControladorVisitante()
        self.btnVisualizarMenu.clicked.connect(self.visualizar_menu)
        self._callback_cerrar_sesion = None
        self.usuario_visitante = UserVo(
            idUser=0,
            nombre="Visitante",
            apellido="Invitado",
            correo=None,
            contrasena=None,
            rol="visitante",
        )

    def cargar_menu_del_dia(self):
        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        platos = self._controlador.obtener_menu_por_fecha(fecha)

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

    def configurar_interfaz(self):
        super().setupUi(self)
        self.setWindowTitle("Menú Visitante")
        self.labelUsuario.setText("¿Qué habrá de comer hoy?")
        self.configurar_calendario()
        self.btnVisualizarMenu.setEnabled(False)
        self.btnVisualizarMenu.clicked.connect(self.visualizar_menu)
        self.btnVolver.clicked.connect(self.volver_al_panel)
        self.btnReservarComida.setVisible(False)
        self.btnReservarComida.clicked.connect(self.confirmar_reserva)

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
        if fecha.dayOfWeek() in (Qt.Saturday, Qt.Sunday) or fecha < QDate.currentDate():
            mostrar_warning(self, "Fecha inválida", "Selecciona un día hábil y no pasado.")
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

    def confirmar_reserva(self):
        def extraer_nombre(item):
            return item.text().split("  (")[0].strip() if item else ""

        primero = extraer_nombre(self.listaPrimeros.currentItem())
        segundo = extraer_nombre(self.listaSegundos.currentItem())
        postre = extraer_nombre(self.listaPostres.currentItem())

        if not (primero and segundo and postre):
            mostrar_warning(self, "Selección incompleta", "Selecciona un primer plato, segundo y postre.")
            return

        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        confirmacion = mostrar_pregunta(self, "Confirmar reserva",
            f"¿Confirmas esta selección?\n\nPrimero: {primero}\nSegundo: {segundo}\nPostre: {postre}")
        if confirmacion != QMessageBox.Yes:
            return

        self._controlador.hacer_reserva_anonima(fecha, primero, segundo, postre)
        mostrar_info(self, "Reserva", "Reserva realizada con éxito.")

        id_reserva = self._controlador.hacer_reserva_anonima(fecha, primero, segundo, postre)
        if id_reserva:
            def callback_pago_exitoso():
                self.abrir_ticket(id_reserva)

            self.pago_window = PagoWindow(self.usuario_visitante, 7.5, "tarjeta", callback_pago_exitoso, id_reserva)
            self.pago_window.show()
        else:
            mostrar_error(self, "Error", "No se pudo registrar la reserva.")

    def volver_al_panel(self):
        if mostrar_pregunta(self, "Confirmación", "¿Volver al inicio?") == QMessageBox.Yes:
            if self._callback_cerrar_sesion:
                self._callback_cerrar_sesion()
            else:
                from src.vista.Login import Login
                self.close()
                self._login = Login()
                self._login.showFullScreen()

    def abrir_ticket(self, id_reserva):
        self.ticket_window = GenerarTicket(id_reserva)
        self.ticket_window.show()