"""All environment-specific values live in settings/app.json (plus env vars for secrets)."""
import json
import os
from dataclasses import dataclass, field
from pathlib import Path

# Placeholder prices in kobo per message (delivery cost + 20%). Confirm with your providers.
DEFAULT_PRICES = {"sms": 800, "whatsapp": 1500, "email": 150}


def _default_settings_file() -> Path:
    """Search upward for settings/app.json (works on a laptop and inside the container)."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "settings" / "app.json"
        if candidate.exists():
            return candidate
    return here.parent.parent / "app_settings.json"


@dataclass(frozen=True)
class Settings:
    env: str
    project_id: str
    web_origin: str
    email_from: str
    first_notice_channels: list = field(default_factory=list)
    default_reminder_channel: str = "sms"
    require_mfa: bool = True
    message_price_kobo: dict = field(default_factory=lambda: dict(DEFAULT_PRICES))


def _mfa_required(env: str) -> bool:
    if env == "local":
        return False
    # Temporary escape hatch for STAGING only, until the MFA sign-in screen exists.
    # Production always requires MFA, whatever the variable says.
    if env == "staging" and os.getenv("REQUIRE_MFA", "true").lower() == "false":
        return False
    return True


def load_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "local")
    path = Path(os.getenv("APP_SETTINGS_FILE") or _default_settings_file())
    data = json.loads(path.read_text())
    merged = {**data["shared"], **data[env]}
    return Settings(
        env=env,
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT", "enterprisesend-local"),
        web_origin=os.getenv("WEB_ORIGIN") or merged["web_origin"],
        email_from=merged["email_from"],
        first_notice_channels=merged["first_notice_channels"],
        default_reminder_channel=merged["default_reminder_channel"],
        message_price_kobo=merged.get("message_price_kobo", dict(DEFAULT_PRICES)),
        require_mfa=_mfa_required(env),
    )
