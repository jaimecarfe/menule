from src.modelo.BussinessObject import BussinessObject
from src.modelo.vo.TicketVo import TicketVo

class ControladorTickets:
    def __init__(self):
        self._modelo = BussinessObject()

    def generar_ticket(self, ticket_vo: TicketVo) -> int | None:
        return self._modelo.ticket_service.generar_ticket(ticket_vo)

    def validar_ticket(self, codigo: str) -> bool:
        return self._modelo.ticket_service.validar_ticket(codigo)

    def generar_pdf_ticket(self, id_reserva):
        return self._modelo.ticket_service.generar_pdf_ticket(id_reserva)

    def enviar_ticket_por_correo(self, id_reserva, correo):
        return self._modelo.ticket_service.enviar_ticket_por_correo(id_reserva, correo)

    def obtener_datos_ticket(self, id_reserva):
        return self._modelo.ticket_service.obtener_datos_ticket(id_reserva)

    def es_reserva_de_visitante(self, id_reserva) -> bool:
        return self._modelo.ticket_service.es_reserva_de_visitante(id_reserva)