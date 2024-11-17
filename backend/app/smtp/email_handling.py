import smtplib
from email.mime.text import MIMEText
from pydantic import EmailStr
from ..settings import application_settings


def send_email(to: EmailStr, subject: str, content: str, from_: str = "MoneyGuard Team <hello@demomailtrap.com>"):

    message = MIMEText(content)
    message["From"] = from_
    message["To"] = to
    message["Subject"] = subject

    with smtplib.SMTP(application_settings.smtp_server_host, application_settings.smtp_server_port) as server:
        server.starttls()
        server.login(application_settings.smtp_server_login, application_settings.smtp_server_password)
        server.sendmail(from_, to, message.as_string())