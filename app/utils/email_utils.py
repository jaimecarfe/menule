# app/utils/email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(destino: str, asunto: str, cuerpo: str):
    """
    Envía un correo electrónico al destinatario.
    Configura tus credenciales SMTP o usa print para entorno de desarrollo.
    """
    try:
        # Configuración SMTP (Modificar con credenciales reales si dispones de servidor)
        # smtp_server = "smtp.gmail.com"
        # smtp_port = 587
        # remitente = "tu_correo@gmail.com"
        # password = "tu_password_de_aplicacion"

        # Para desarrollo / pruebas locales:
        print(f"--- [EMAIL SIMULADO ENVIADO A {destino}] ---")
        print(f"Asunto: {asunto}")
        print(f"Cuerpo:\n{cuerpo}")
        print("---------------------------------------------")
        
        # Código SMTP real (Descomentar en producción):
        # msg = MIMEMultipart()
        # msg['From'] = remitente
        # msg['To'] = destino
        # msg['Subject'] = asunto
        # msg.attach(MIMEText(cuerpo, 'plain'))
        #
        # server = smtplib.SMTP(smtp_server, smtp_port)
        # server.starttls()
        # server.login(remitente, password)
        # server.sendmail(remitente, destino, msg.as_string())
        # server.quit()

    except Exception as e:
        print(f"Error al enviar el correo a {destino}: {e}")