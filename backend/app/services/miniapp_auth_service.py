from __future__ import annotations


class MiniAppAuthService:
    def validate(self, init_data: str) -> bool:
        return bool(init_data)
