"""Local demo only: pretends every message was accepted and prints it to the console."""
import logging

from .base import Adapter, SendResult

log = logging.getLogger("delivery")


class LogAdapter(Adapter):
    name = "log"

    def __init__(self, channel: str):
        self.channel = channel

    def send(self, to, message, subject=""):
        log.warning("[pretend %s] to=%s :: %s", self.channel, to, message)
        return SendResult(True, f"log-{abs(hash((to, message)))}")
