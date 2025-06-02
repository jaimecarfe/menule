import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_correo(destino, asunto, mensaje):
    remitente = "comedormenule@gmail.com"
    contraseña = os.environ.get("EMAIL_PASSWORD")

    if not contraseña:
        raise ValueError("No se encontró la variable de entorno EMAIL_PASSWORD")

    msg = MIMEText(mensaje, 'plain', 'utf-8')
    msg['Subject'] = Header(asunto, 'utf-8')
    msg['From'] = formataddr((str(Header('MenULE', 'utf-8')), remitente))
    msg['To'] = destino

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(remitente, contraseña)
        smtp.sendmail(remitente, [destino], msg.as_string())

def enviar_ticket_por_correo(destino, asunto, mensaje, ruta_adjunto):
    pass  # Pendiente implementar adjuntos
