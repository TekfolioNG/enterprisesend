import os

from .log import LogAdapter
from .resend import ResendEmail
from .termii import TermiiSms
from .whatsapp import WhatsAppStub


def build_adapters(settings) -> dict:
    """Swap a provider here (or via settings later) without touching business logic."""
    if os.getenv("DELIVERY_MODE") == "log":
        if settings.env != "local":
            raise RuntimeError("DELIVERY_MODE=log is for local development only")
        return {c: LogAdapter(c) for c in ("sms", "whatsapp", "email")}
    return {"sms": TermiiSms(), "whatsapp": WhatsAppStub(),
            "email": ResendEmail(settings.email_from)}
