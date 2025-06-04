from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox
from src.modelo.dao.TicketDao import TicketDao
from src.utils.ticket_generator import generar_ticket_pdf
from src.utils.email_utils import enviar_correo
import os

class GenerarTicket(QWidget):
    def __init__(self, id_reserva):
        super().__init__()
        self.id_reserva = id_reserva
        self.setWindowTitle("Generar Ticket")

        self.btn_generar = QPushButton("Generar PDF")
        self.btn_enviar = QPushButton("Enviar por correo")

        self.btn_generar.clicked.connect(self.generar_pdf)
        self.btn_enviar.clicked.connect(self.enviar_por_correo)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_generar)
        layout.addWidget(self.btn_enviar)
        self.setLayout(layout)

    def generar_pdf(self):
        dao = TicketDao()
        datos = dao.obtener_datos_ticket(self.id_reserva)
        if not datos or len(datos) < 5:
            QMessageBox.warning(self, "Error", "No hay datos suficientes para esta reserva.")
            return

        ticket_data = {
            "ID": datos[0],
            "Nombre": datos[1],
            "Email": datos[2],
            "Fecha": datos[3],
            "Total": f"{datos[4]} EUR"
        }

        from pathlib import Path
        carpeta_descargas = str(Path.home() / "Downloads")
        ruta = os.path.join(carpeta_descargas, f"ticket_reserva_{datos[1]}.pdf")

        generar_ticket_pdf(ticket_data, ruta)
        QMessageBox.information(self, "Listo", f"Ticket guardado como {ruta}")

    def enviar_por_correo(self):
        dao = TicketDao()
        datos = dao.obtener_datos_ticket(self.id_reserva)
        if not datos or len(datos) < 5:
            QMessageBox.warning(self, "Error", "No hay datos suficientes para esta reserva.")
            return

        ticket_data = {
            "ID": datos[0],
            "Nombre": datos[1],
            "Email": datos[2],
            "Fecha": datos[3],
            "Total": f"{datos[4]} EUR"
        }

        ruta = f"ticket_reserva_{datos[0]}.pdf"
        generar_ticket_pdf(ticket_data, ruta)

        try:
            enviar_correo(
                destino=datos[2],
                asunto="¡Tu ticket de reserva está aquí!",
                cuerpo="¡Hola! 🎉\n\nGracias por reservar con nosotros. Aquí tienes tu ticket de reserva adjunto. ¡Esperamos que disfrutes de tu experiencia!\n\nSaludos cordiales,\nEl equipo de reservas",
                archivo_adjunto=ruta
            )
            QMessageBox.information(self, "Enviado", "Ticket enviado por correo.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo enviar: {e}")
        finally:
            if os.path.exists(ruta):
                os.remove(ruta)