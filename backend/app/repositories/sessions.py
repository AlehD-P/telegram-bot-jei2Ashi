from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.session import Session as BotSession


class SessionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, bot_session: BotSession) -> BotSession:
        self.session.add(bot_session)
        self.session.flush()
        return bot_session
