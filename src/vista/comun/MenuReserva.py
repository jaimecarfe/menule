from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorEstudiante import ControladorEstudiante
from src.vista.comun.ReservaComida import ReservaComida
from src.modelo.vo.ReservaVo import ReservaVo
from src.vista.comun.PagoWindow import PagoWindow
from src.vista.comun.GenerarTicket import GenerarTicket
from PyQt5 import uic
from src.controlador.ControladorProfesor import ControladorProfesor


Form, Window = uic.loadUiType("./src/vista/ui/MenuEstudiante.ui")

class MenuEstudiante(VentanaBase, Form):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = usuario
        if self.usuario.rol == "estudiante":
            self._controlador = ControladorEstudiante()
        elif self.usuario.rol == "profesor":
            self._controlador = ControladorProfesor()
        self._callback_cerrar_sesion = None
        self.setupUi(self)
        self.configurar_interfaz()

    def configurar_interfaz(self):
        self.setWindowTitle("Menú Estudiante")
        self.labelUsuario.setText(f"¿Qué habrá de comer hoy, {self.usuario.nombre}?")
        self.configurar_calendario()

        self.btnVisualizarMenu.setEnabled(False)
        self.btnVisualizarMenu.clicked.connect(self.visualizar_menu)
        self.btnVolver.clicked.connect(self.volver_al_panel)
        self.btnReservarComida.setVisible(False)
        self.btnReservarComida.clicked.connect(self.confirmar_reserva)
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
        if fecha.isValid():
            self.cargar_menu_del_dia()
            self.btnReservarComida.setVisible(True)
        else:
            QMessageBox.information(self, "Sin fecha", "Por favor selecciona un día válido.")
            self.btnReservarComida.setVisible(False)

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

    def confirmar_reserva(self):
        primero_item = self.listaPrimeros.currentItem()
        segundo_item = self.listaSegundos.currentItem()
        postre_item = self.listaPostres.currentItem()

        if not primero_item or not segundo_item or not postre_item:
            QMessageBox.warning(self, "Selección incompleta", "Debes seleccionar un primer plato, un segundo y un postre antes de reservar.")
            return

        primero = primero_item.text().split("  (")[0].strip()
        segundo = segundo_item.text().split("  (")[0].strip()
        postre = postre_item.text().split("  (")[0].strip()
        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")

        # Mostrar resumen de selección (informativo, no pregunta todavía)
        QMessageBox.information(
            self,
            "Resumen de selección",
            f"Has seleccionado:\n\n"
            f"Primer plato: {primero}\n"
            f"Segundo plato: {segundo}\n"
            f"Postre: {postre}\n"
            f"Fecha: {fecha}"
        )

        # Confirmación final
        respuesta = QMessageBox.question(
            self,
            "¿Confirmar reserva?",
            "¿Deseas continuar con el pago y completar la reserva?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return

        # Calcular precio y método según el rol
        if self.usuario.rol == "estudiante":
            precio = 5.5
            metodo = "tui"
        elif self.usuario.rol == "profesor":
            precio = 6.5
            metodo = "tui"
        else:
            precio = 7.5
            metodo = "tarjeta"

        # Callback tras pago exitoso → hacer reserva y generar ticket
        def callback_pago_exitoso():
            exito = self._controlador.hacer_reserva_completa(self.usuario.idUser, fecha, primero, segundo, postre)
            if exito:
                QMessageBox.information(self, "Reserva hecha", "Reserva registrada con éxito.")
                self.abrir_ticket()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la reserva.")

        # Abrir ventana de pago
        self.pago_window = PagoWindow(self.usuario, precio, metodo, callback_pago_exitoso, id_reserva=None)
        self.pago_window.show()

    def abrir_reserva_comida(self, primero, segundo, postre):
        reserva_comida = ReservaComida(self.usuario, self, primero, segundo, postre)
        reserva_comida.show()

    def volver_al_panel(self):
        if self.parent():
            self.parent().show()
        self.close()

    def reservar_menu(self):
        id_menu = self.obtener_id_menu_seleccionado()  # obtén el ID del menú seleccionado en la UI
        reserva = ReservaVo()
        reserva.id_usuario = self.usuario_actual.id  # o self.usuario.id
        reserva.id_menu = id_menu
        reserva.estado = "pendiente"
        
        self.controlador.crear_reserva(reserva)
        QMessageBox.information(self, "Reserva", "Reserva realizada con éxito.")

    def finalizar_reserva(self, primero, segundo, postre, fecha):
        exito = self._controlador.hacer_reserva_completa(self.usuario.idUser, fecha, primero, segundo, postre)
        if exito:
            QMessageBox.information(self, "Reserva hecha", "Reserva registrada con éxito.")
            self.abrir_ticket()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la reserva.")

    def abrir_ticket(self):
        id_reserva = self._controlador.obtener_ultima_reserva_id(self.usuario.idUser)
        if id_reserva:
            self.ticket_window = GenerarTicket(id_reserva)
            self.ticket_window.show()

