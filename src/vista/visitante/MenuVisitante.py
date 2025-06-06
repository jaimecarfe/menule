from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from src.vista.VentanaBase import VentanaBase
from src.controlador.ControladorVisitante import ControladorVisitante
from PyQt5 import uic
from src.modelo.dao.MenuDao import MenuDao
from src.vista.comun.PagoWindow import PagoWindow
from src.modelo.vo.UserVo import UserVo
from src.vista.comun.GenerarTicket import GenerarTicket
from src.vista.visitante.IntroducirCorreoDialog import IntroducirCorreoDialog
from src.utils.email_utils import enviar_correo

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
        dao = MenuDao()
        platos = dao.obtener_platos_por_fecha(fecha)

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

        respuesta = QMessageBox.question(
            self,
            "Confirmar selección",
            f"¿Quieres reservar este menú?\n\n"
            f"Primero: {primero}\nSegundo: {segundo}\nPostre: {postre}",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            # Calcular precio y método según el rol
            precio = 7.5
            metodo = "tarjeta"

            # --- PRIMERO CREA LA RESERVA Y OBTÉN EL ID ---
            id_reserva = self._controlador.hacer_reserva_anonima(fecha, primero, segundo, postre)
            if id_reserva:
                QMessageBox.information(self, "Reserva hecha", "Reserva registrada con éxito.")

                # Callback tras pago exitoso
                def callback_pago_exitoso():
                    self.abrir_ticket(id_reserva)

                print("Abriendo ventana de pago")
                self.pago_window = PagoWindow(self.usuario_visitante, precio, metodo, callback_pago_exitoso, id_reserva)
                self.pago_window.show()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la reserva.")
           
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
        
    def abrir_ticket(self, id_reserva):
        # Mostrar el ticket
        self.ticket_window = GenerarTicket(id_reserva)
        self.ticket_window.show()

        # Pedir el correo y enviar el ticket por correo
        dialog = IntroducirCorreoDialog(self)
        if dialog.exec_():
            correo = dialog.correo

            # Aquí debes obtener la ruta del PDF generado por GenerarTicket
            # Suponemos que GenerarTicket tiene un método o atributo para la ruta del PDF:
            if hasattr(self.ticket_window, 'ruta_pdf'):
                archivo_pdf = self.ticket_window.ruta_pdf
            elif hasattr(self.ticket_window, 'generar_pdf'):
                archivo_pdf = self.ticket_window.generar_pdf()
            else:
                archivo_pdf = None

            asunto = "¡Hola! 🎉"
            cuerpo = (
                "¡Hola! 🎉\n\n"
                "Gracias por reservar con nosotros. Aquí tienes tu ticket de reserva adjunto. ¡Esperamos que disfrutes de tu experiencia!\n\n"
                "Saludos cordiales,\n"
                "El equipo de reservas"
            )

            try:
                status = enviar_correo(destino=correo, asunto=asunto, cuerpo=cuerpo, archivo_adjunto=archivo_pdf)
                if 200 <= status < 300:
                    QMessageBox.information(self, "Correo enviado", "El tíquet ha sido enviado a tu correo.")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo enviar el correo.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error enviando el correo: {e}")