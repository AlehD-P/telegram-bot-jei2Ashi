from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TelegramChat(BaseModel):
    id: int
    type: str | None = None
    title: str | None = None


class TelegramUser(BaseModel):
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None


class TelegramMessage(BaseModel):
    message_id: int
    chat: TelegramChat
    text: str | None = None
    from_user: TelegramUser | None = Field(default=None, alias="from")


class TelegramUpdate(BaseModel):
    update_id: int
    message: TelegramMessage | None = None
    raw: dict[str, Any] | None = None
