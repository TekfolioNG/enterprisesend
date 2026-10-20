"""All environment-specific values live in settings/app.json (plus env vars for secrets)."""
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_FILE = Path(__file__).resolve().parents[3] / "settings" / "app.json"


@dataclass(frozen=True)
class Settings:
    env: str
    project_id: str
    web_origin: str
    email_from: str
    ai_model: str
    ai_location: str
    first_notice_channels: list = field(default_factory=list)
    default_reminder_channel: str = "sms"
    require_mfa: bool = True


def load_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "local")
    path = Path(os.getenv("APP_SETTINGS_FILE", DEFAULT_FILE))
    data = json.loads(path.read_text())
    merged = {**data["shared"], **data[env]}
    return Settings(
        env=env,
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT", "enterprisesend-local"),
        web_origin=merged["web_origin"],
        email_from=merged["email_from"],
        ai_model=merged["ai_model"],
        ai_location=merged["ai_location"],
        first_notice_channels=merged["first_notice_channels"],
        default_reminder_channel=merged["default_reminder_channel"],
        require_mfa=(env != "local"),  # enforced on staging and production
    )
