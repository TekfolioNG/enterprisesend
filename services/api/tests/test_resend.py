from adapters import resend as mod


class FakeResp:
    def __init__(self, code, body=None):
        self.status_code, self._body = code, body or {}

    def json(self):
        return self._body


def test_not_configured(monkeypatch):
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    res = mod.ResendEmail("a@b.com").send("x@y.com", "hi")
    assert not res.ok and res.error == "email_not_configured"


def test_accepted_and_failure(monkeypatch):
    monkeypatch.setenv("RESEND_API_KEY", "k")
    sent = {}

    def fake_post(url, **kw):
        sent.update(kw["json"])
        return FakeResp(200, {"id": "abc"})

    monkeypatch.setattr(mod.requests, "post", fake_post)
    res = mod.ResendEmail("billing@enterprisesend.com").send("x@y.com", "hi", "Your bill")
    assert res.ok and res.provider_ref == "abc"
    assert sent["from"] == "EnterpriseSend <billing@enterprisesend.com>" and sent["to"] == ["x@y.com"]

    monkeypatch.setattr(mod.requests, "post", lambda *a, **k: FakeResp(422))
    assert mod.ResendEmail("a@b.com").send("x@y.com", "hi").error == "http_422"
