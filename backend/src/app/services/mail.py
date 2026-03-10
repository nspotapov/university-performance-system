import logging
import smtplib
from email.message import EmailMessage
from typing import Sequence

from app.core.config import settings


class MailService:
    def __init__(self):
        self.__server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

    async def send_mail(self, to_addrs: str | Sequence[str], subject: str, content: str):
        try:
            if settings.SMTP_TLS:
                self.__server.starttls()

            self.__server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

            email_msg = EmailMessage()
            email_msg.set_content(content)
            email_msg["Subject"] = subject
            # email_msg["From"] = settings.SMTP_FROM

            self.__server.send_message(
                email_msg,
                to_addrs=to_addrs,
                from_addr=settings.SMTP_FROM
            )

            self.__server.quit()

        except Exception as ex:
            logging.warn(str(ex))
