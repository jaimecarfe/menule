import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv
import base64

load_dotenv()

def enviar_correo(destino, asunto, cuerpo, archivo_adjunto=None):
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la variable de entorno SENDGRID_API_KEY")
    
    message = Mail(
        from_email='comedormenule@gmail.com',
        to_emails=destino,
        subject=asunto,
        plain_text_content=cuerpo
    )
    
    # Adjuntar archivo si existe
    if archivo_adjunto and os.path.exists(archivo_adjunto):
        with open(archivo_adjunto, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
            attachment = Attachment(
                FileContent(encoded),
                FileName(os.path.basename(archivo_adjunto)),
                FileType("application/pdf"),
                Disposition("attachment")
            )
            message.attachment = attachment
    
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        raise RuntimeError(f"Error enviando correo: {e}")