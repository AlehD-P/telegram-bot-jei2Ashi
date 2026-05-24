from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import Chat


class ChatRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_telegram_chat_id(self, telegram_chat_id: int) -> Chat | None:
        return self.session.scalar(select(Chat).where(Chat.telegram_chat_id == telegram_chat_id))

    def save(self, chat: Chat) -> Chat:
        self.session.add(chat)
        self.session.flush()
        return chat
