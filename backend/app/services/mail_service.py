import logging
import smtplib
from email.message import EmailMessage
from typing import Sequence

from app import config


class MailService:
    def __init__(self):
        self._server = None

    async def send_mail(self, to_addr: str | Sequence[str], subject: str, content: str):
        try:
            self._server = smtplib.SMTP(config.smtp_host, config.smtp_port)

            # self._server.starttls()
            self._server.login(config.smtp_username, config.smtp_password)

            email_msg = EmailMessage()
            email_msg.set_content(content)
            email_msg["Subject"] = subject
            email_msg["From"] = config.smtp_from

            self._server.send_message(email_msg, to_addrs=to_addr, from_addr=config.smtp_from)

            self._server.quit()

        except Exception as e:
            logging.warn(str(e))
