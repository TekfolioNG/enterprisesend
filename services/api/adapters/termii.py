import os

import requests

from .base import Adapter, SendResult


class TermiiSms(Adapter):
    channel, name = "sms", "termii"

    def __init__(self):
        # Confirm base URL and endpoint in Termii's current docs for your account.
        self.base = os.getenv("TERMII_BASE_URL", "https://api.ng.termii.com")
        self.key = os.getenv("TERMII_API_KEY", "")
        self.sender = os.getenv("TERMII_SENDER_ID", "")

    def send(self, to, message, subject=""):
        if not self.key or not self.sender:
            return SendResult(False, error="sms_not_configured")
        try:
            r = requests.post(f"{self.base}/api/sms/send", timeout=10, json={
                "to": to, "from": self.sender, "sms": message,
                "type": "plain", "channel": "generic", "api_key": self.key})
            if r.status_code == 200:
                return SendResult(True, r.json().get("message_id", ""))
            return SendResult(False, error=f"http_{r.status_code}")
        except Exception as exc:
            return SendResult(False, error=type(exc).__name__)
