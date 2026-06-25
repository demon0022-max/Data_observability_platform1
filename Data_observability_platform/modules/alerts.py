
import smtplib
from email.mime.text import MIMEText

def send_email_alert(message):
    sender = "your_email@gmail.com"
    receiver = "receiver_email@gmail.com"
    password = "your_app_password"

    msg = MIMEText(message)
    msg["Subject"] = "Data Observability Alert"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email alert failed:", e)
