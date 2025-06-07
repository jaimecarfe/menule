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
            QMessageBox.warning(self, "Fecha inválida", "Selecciona un día hábil y no pasado.")
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
            QMessageBox.warning(self, "Selección incompleta", "Selecciona un primer plato, segundo y postre.")
            return

        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        confirmacion = QMessageBox.question(self, "Confirmar reserva",
            f"¿Confirmas esta selección?\n\nPrimero: {primero}\nSegundo: {segundo}\nPostre: {postre}",
            QMessageBox.Yes | QMessageBox.No)
        if confirmacion != QMessageBox.Yes:
            return

        self._controlador.hacer_reserva_anonima(fecha, primero, segundo, postre)
        QMessageBox.information(self, "Reserva", "Reserva realizada con éxito.")

        id_reserva = self._controlador.hacer_reserva_anonima(fecha, primero, segundo, postre)
        if id_reserva:
            def callback_pago_exitoso():
                self.abrir_ticket(id_reserva)

            self.pago_window = PagoWindow(self.usuario_visitante, 7.5, "tarjeta", callback_pago_exitoso, id_reserva)
            self.pago_window.show()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la reserva.")

    def volver_al_panel(self):
        if QMessageBox.question(self, "Confirmación", "¿Volver al inicio?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
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
