from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_telegram_user_id(self, telegram_user_id: int) -> User | None:
        return self.session.scalar(select(User).where(User.telegram_user_id == telegram_user_id))

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        return user
