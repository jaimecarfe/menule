from fpdf import FPDF
import qrcode
import os

def generar_ticket_pdf(ticket_data, ruta_salida):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Ticket de Reserva", ln=True, align='C')
    pdf.ln(10)

    for key, value in ticket_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Generar QR
    qr = qrcode.make(f"Reserva #{ticket_data['ID']}")
    qr_path = "qr_temp.png"
    qr.save(qr_path)
    pdf.image(qr_path, x=80, y=100, w=50)
    os.remove(qr_path)

    pdf.output(ruta_salida)
