from src.modelo.dao.TicketDao import TicketDao
from src.modelo.vo.TicketVo import TicketVo
from src.utils.ticket_generator import generar_ticket_pdf
from src.utils.email_utils import enviar_correo
from src.modelo.dao.PagoDao import PagoDao
from src.modelo.dao.ReservaDao import ReservaDao
from pathlib import Path
import os

class LogicaTicket:
    def __init__(self):
        self.ticket_dao = TicketDao()
        self.pago_dao = PagoDao()
        self.reserva_dao = ReservaDao()

    def generar_ticket(self, ticket_vo: TicketVo) -> int | None:
        return self.ticket_dao.insert(ticket_vo)

    def validar_ticket(self, codigo: str) -> bool:
        return self.ticket_dao.marcar_usado(codigo)

    def obtener_datos_ticket(self, id_reserva):
        return self.ticket_dao.obtener_datos_ticket(id_reserva)

    def generar_pdf_ticket(self, id_reserva):
        datos = self.obtener_datos_ticket(id_reserva)
        if not datos or len(datos) < 5:
            return None

        ticket_data = {
            "ID": datos[0],
            "Nombre": datos[1],
            "Email": datos[2],
            "Fecha": datos[3],
            "Total": f"{datos[4]} EUR"
        }

        carpeta_descargas = str(Path.home() / "Downloads")
        ruta = os.path.join(carpeta_descargas, f"ticket_reserva_{datos[1]}.pdf")
        generar_ticket_pdf(ticket_data, ruta)
        return ruta

    def enviar_ticket_por_correo(self, id_reserva, correo):
        ruta = self.generar_pdf_ticket(id_reserva)
        if not ruta:
            return False, "No se pudo generar el PDF del ticket."

        asunto = "¡Tu ticket de reserva está aquí!"
        cuerpo = (
            "¡Hola! 🎉\n\n"
            "Gracias por reservar con nosotros. Aquí tienes tu ticket de reserva adjunto.\n\n"
            "Saludos,\nEl equipo de MenULE"
        )

        try:
            status = enviar_correo(destino=correo, asunto=asunto, cuerpo=cuerpo, archivo_adjunto=ruta)
            if 200 <= status < 300:
                return True, None
            else:
                return False, "Error al enviar el correo."
        except Exception as e:
            return False, str(e)
        finally:
            if os.path.exists(ruta):
                os.remove(ruta)

    def es_reserva_de_visitante(self, id_reserva: int) -> bool:
            return self.reserva_dao.es_reserva_de_visitante(id_reserva)    

