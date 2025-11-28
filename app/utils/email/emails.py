import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from pathlib import Path


TEMPLATE_PATH = Path(__file__).parent / "otp_template.html"

def send_otp(email: str, otp: str) -> bool:
    # Load HTML template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Replace placeholder with actual OTP
    html_content = html_content.replace("{{OTP}}", str(otp))

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Your Verification Code: {otp}"
    message["From"] = settings.SENDER_EMAIL
    message["To"] = email

    # Plain text fallback
    plain_text = f"Your verification code is: {otp}\nThis code expires in 10 minutes."

    message.attach(MIMEText(plain_text, "plain"))
    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.SENDER_EMAIL, settings.APP_PASSWORD)
            server.sendmail(settings.SENDER_EMAIL, email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email")
        return False