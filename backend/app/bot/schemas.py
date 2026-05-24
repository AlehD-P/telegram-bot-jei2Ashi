from __future__ import annotations

from pydantic import BaseModel


class TelegramUpdate(BaseModel):
    update_id: int
