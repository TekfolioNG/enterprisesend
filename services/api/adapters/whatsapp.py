from .base import Adapter, SendResult


class WhatsAppStub(Adapter):
    """Placeholder until the provider (Meta Cloud API or a BSP) and templates are approved."""
    channel, name = "whatsapp", "stub"

    def send(self, to, message, subject=""):
        return SendResult(False, error="whatsapp_not_enabled")
