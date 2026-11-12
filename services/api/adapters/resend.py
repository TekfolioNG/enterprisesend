import os

import requests

from .base import Adapter, SendResult


class ResendEmail(Adapter):
    channel, name = "email", "resend"

    def __init__(self, from_email: str, from_name: str = "EnterpriseSend"):
        self.key = os.getenv("RESEND_API_KEY", "")
        # The sending domain must be verified in Resend, or the API refuses the message.
        self.sender = f"{from_name} <{from_email}>"

    def send(self, to, message, subject=""):
        if not self.key:
            return SendResult(False, error="email_not_configured")
        try:
            r = requests.post("https://api.resend.com/emails", timeout=10,
                headers={"Authorization": f"Bearer {self.key}"},
                json={"from": self.sender, "to": [to],
                      "subject": subject or "Notification", "text": message})
            if r.status_code == 200:
                return SendResult(True, r.json().get("id", ""))
            return SendResult(False, error=f"http_{r.status_code}")
        except Exception as exc:
            return SendResult(False, error=type(exc).__name__)
