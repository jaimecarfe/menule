import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def enviar_correo(destino, asunto, mensaje):
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la variable de entorno SENDGRID_API_KEY")
    
    message = Mail(
        from_email='comedormenule@gmail.com',
        to_emails=destino,
        subject=asunto,
        plain_text_content=mensaje
    )
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        raise RuntimeError(f"Error enviando correo: {e}")
    
def enviar_ticket_por_correo():
    pass