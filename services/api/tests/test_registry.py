import pytest

from adapters.registry import build_adapters
from app.config import load_settings


def test_log_mode_pretends_success_locally(monkeypatch):
    monkeypatch.setenv("DELIVERY_MODE", "log")
    monkeypatch.setenv("ENVIRONMENT", "local")
    adapters = build_adapters(load_settings())
    assert all(a.send("x", "hello").ok for a in adapters.values())


def test_log_mode_is_refused_outside_local(monkeypatch):
    monkeypatch.setenv("DELIVERY_MODE", "log")
    monkeypatch.setenv("ENVIRONMENT", "staging")
    with pytest.raises(RuntimeError):
        build_adapters(load_settings())
