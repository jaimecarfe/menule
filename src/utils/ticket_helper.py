from src.utils.ticket_generator import generar_ticket_pdf
from src.utils.email_utils import enviar_correo
from src.modelo.dao.TicketDao import TicketDao
from pathlib import Path
import os

def generar_y_enviar_ticket(id_reserva, correo_destino):
    dao = TicketDao()
    datos = dao.obtener_datos_ticket(id_reserva)
    if not datos or len(datos) < 5:
        return False, "Datos insuficientes para la reserva."

    ticket_data = {
        "ID": datos[0],
        "Nombre": datos[1],
        "Email": correo_destino,
        "Fecha": datos[3],
        "Total": f"{datos[4]} EUR"
    }

    carpeta_descargas = str(Path.home() / "Downloads")
    ruta_pdf = os.path.join(carpeta_descargas, f"ticket_reserva_{datos[0]}.pdf")
    generar_ticket_pdf(ticket_data, ruta_pdf)

    asunto = "¡Tu ticket de reserva está aquí!"
    cuerpo = (
        "¡Hola! 🎉\n\n"
        "Gracias por reservar con nosotros. Aquí tienes tu ticket de reserva adjunto.\n\n"
        "Saludos,\nEl equipo de reservas"
    )

    try:
        status = enviar_correo(destino=correo_destino, asunto=asunto, cuerpo=cuerpo, archivo_adjunto=ruta_pdf)
        if 200 <= status < 300:
            return True, None
        else:
            return False, "Error en el envío del correo."
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(ruta_pdf):
            os.remove(ruta_pdf)
