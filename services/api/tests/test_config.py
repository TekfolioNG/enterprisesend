import pytest

from app.config import load_settings


def test_local_never_needs_mfa(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "local")
    assert load_settings().require_mfa is False


def test_staging_requires_mfa_by_default(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "staging")
    monkeypatch.delenv("REQUIRE_MFA", raising=False)
    assert load_settings().require_mfa is True


def test_staging_can_temporarily_turn_mfa_off(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "staging")
    monkeypatch.setenv("REQUIRE_MFA", "false")
    assert load_settings().require_mfa is False


def test_production_ignores_the_mfa_override(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("REQUIRE_MFA", "false")
    assert load_settings().require_mfa is True


def test_web_origin_can_be_overridden(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "staging")
    monkeypatch.setenv("WEB_ORIGIN", "https://example-web.run.app")
    assert load_settings().web_origin == "https://example-web.run.app"


def test_settings_file_can_come_from_an_env_variable(monkeypatch, tmp_path):
    import json, shutil
    from app.config import _default_settings_file
    copy = tmp_path / "elsewhere.json"
    shutil.copy(_default_settings_file(), copy)
    monkeypatch.setenv("ENVIRONMENT", "staging")
    monkeypatch.setenv("APP_SETTINGS_FILE", str(copy))
    assert load_settings().env == "staging"


def test_default_settings_file_is_found_without_a_fixed_depth():
    from app.config import _default_settings_file
    assert _default_settings_file().name == "app.json"
