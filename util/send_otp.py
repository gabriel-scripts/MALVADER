import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from dotenv import load_dotenv
load_dotenv(override=True)

smtp_server = os.getenv("smtp_server")
smtp_port = os.getenv("smtp_port")
sender_email = os.getenv("sender_email")  
sender_password = os.getenv("sender_password")  

async def send_otp(recipient_email: str, otp: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Seu código OTP"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    html = f"""
    <html>
      <body>
        <p>Olá!</p>
        <p>Seu código <b>OTP</b> é:</p>
        <h2 style="color: #2d89ef;">{otp}</h2>
        <p><b>Atenção:</b> Este código expira em <b>5 minutos</b>.</p>
        <p>Não compartilhe este código com ninguém.</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"[Error] send_otp error: {e}")