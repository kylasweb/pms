from pydantic import BaseModel
import resend
from src.config import config_instance


class EmailModel(BaseModel):
    from_: str
    to_: str | None
    subject_: str
    html_: str


settings = config_instance().EMAIL_SETTINGS


class SendMail:
    def __init__(self):
        self._resend = resend
        self._resend.api_key = settings.RESEND.API_KEY

    async def send_mail_resend(self, email: EmailModel):
        params = {'from': email.from_, 'to': email.to_, 'subject': email.subject_, 'html': email.subject_}
        self._resend.Emails.send(params=params)
