from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.users import UserRepository


class UserService:
    def __init__(self, session: Session) -> None:
        self.repository = UserRepository(session)

    def get_or_create_user(self, telegram_user_id: int, username: str | None) -> User:
        user = self.repository.get_by_telegram_user_id(telegram_user_id)
        if user is not None:
            user.username = username
            return user
        return self.repository.save(User(telegram_user_id=telegram_user_id, username=username))
