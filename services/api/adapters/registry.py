from .sendgrid import SendGridEmail
from .termii import TermiiSms
from .whatsapp import WhatsAppStub


def build_adapters(settings) -> dict:
    """Swap a provider here (or via settings later) without touching business logic."""
    return {"sms": TermiiSms(), "whatsapp": WhatsAppStub(),
            "email": SendGridEmail(settings.email_from)}
