import aiosmtplib
from email.mime.text import MIMEText
from pydantic import EmailStr
from ..settings import application_settings


async def send_email(
    to: EmailStr,
    subject: str,
    content: str,
    from_: str = "MoneyGuard Team <hello@demomailtrap.com>",
):
    message = MIMEText(content)
    message["From"] = from_
    message["To"] = to
    message["Subject"] = subject

    smtp_client = aiosmtplib.SMTP(
        hostname=application_settings.smtp_server_host,
        port=application_settings.smtp_server_port,
    )

    await smtp_client.connect()
    await smtp_client.login(
        application_settings.smtp_server_login,
        application_settings.smtp_server_password,
    )
    try:
        await smtp_client.sendmail(from_, to, message.as_string())
    except Exception as ex:
        print(f"Couldn't send email to: {to}. Cause: {ex}")
    finally:
        await smtp_client.quit()
