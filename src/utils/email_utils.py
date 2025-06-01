import smtplib
from email.message import EmailMessage

def enviar_ticket_por_correo(destino, asunto, cuerpo, archivo_adjunto):
    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = "menule@tuapp.com"
    msg['To'] = destino
    msg.set_content(cuerpo)

    with open(archivo_adjunto, "rb") as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename="ticket.pdf")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login("menule@tuapp.com", "CONTRASEÑA_APP")
        smtp.send_message(msg)
