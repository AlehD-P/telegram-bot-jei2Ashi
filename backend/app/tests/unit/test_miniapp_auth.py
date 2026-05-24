import hashlib
import hmac
import json
from urllib.parse import quote

import pytest

from app.config import get_settings
from app.services.miniapp_auth_service import MiniAppAuthService


def _signed_init_data(bot_token: str, payload: dict[str, object]) -> str:
    data = {
        "auth_date": "1710000000",
        "query_id": "AAExampleQueryId",
        "user": json.dumps(payload, separators=(",", ":")),
    }
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    data_hash = hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()
    data["hash"] = data_hash
    return "&".join(f"{k}={quote(v)}" for k, v in data.items())


def test_validate_rejects_missing_init_data() -> None:
    with pytest.raises(ValueError, match="Missing initData"):
        MiniAppAuthService().validate("")


def test_validate_rejects_invalid_signature(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "bot_token", "test-token")

    with pytest.raises(ValueError, match="Invalid initData signature"):
        MiniAppAuthService().validate("user=%7B%22id%22%3A1%7D&hash=bad")


def test_validate_accepts_signed_init_data(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "bot_token", "test-token")

    init_data = _signed_init_data("test-token", {"id": 123, "username": "alice"})
    identity = MiniAppAuthService().validate(init_data)

    assert identity.telegram_user_id == 1
