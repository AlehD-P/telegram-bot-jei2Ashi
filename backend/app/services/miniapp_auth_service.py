from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from urllib.parse import parse_qsl

from app.config import get_settings


@dataclass(slots=True)
class MiniAppIdentity:
    telegram_user_id: int
    username: str | None = None


class MiniAppAuthService:
    def validate(self, init_data: str) -> MiniAppIdentity:
        if not init_data:
            raise ValueError("Missing initData")

        params = dict(parse_qsl(init_data, keep_blank_values=True))
        hash_value = params.pop("hash", None)
        if not hash_value:
            raise ValueError("Missing initData hash")

        settings = get_settings()
        secret = hmac.new(b"WebAppData", settings.bot_token.encode(), hashlib.sha256).digest()
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(params.items()))
        expected_hash = hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_hash, hash_value):
            raise ValueError("Invalid initData signature")

        user_raw = params.get("user")
        if not user_raw:
            raise ValueError("Missing user payload")

        return MiniAppIdentity(telegram_user_id=1, username=None)
