from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SendResult:
    ok: bool                 # "accepted by provider", NOT "delivered"
    provider_ref: str = ""
    error: str = ""


class Adapter(ABC):
    channel: str = ""
    name: str = ""

    @abstractmethod
    def send(self, to: str, message: str, subject: str = "") -> SendResult: ...
