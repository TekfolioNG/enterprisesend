import os

import requests

from .base import Adapter, SendResult


class SendGridEmail(Adapter):
    channel, name = "email", "sendgrid"

    def __init__(self, from_email: str, from_name: str = "EnterpriseSend"):
        self.key = os.getenv("SENDGRID_API_KEY", "")
        self.from_email, self.from_name = from_email, from_name

    def send(self, to, message, subject=""):
        if not self.key:
            return SendResult(False, error="email_not_configured")
        try:
            r = requests.post("https://api.sendgrid.com/v3/mail/send", timeout=10,
                headers={"Authorization": f"Bearer {self.key}"},
                json={"personalizations": [{"to": [{"email": to}]}],
                      "from": {"email": self.from_email, "name": self.from_name},
                      "subject": subject or "Notification",
                      "content": [{"type": "text/plain", "value": message}]})
            if r.status_code == 202:
                return SendResult(True, r.headers.get("X-Message-Id", ""))
            return SendResult(False, error=f"http_{r.status_code}")
        except Exception as exc:
            return SendResult(False, error=type(exc).__name__)
