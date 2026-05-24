from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.update_log import UpdateLog


class UpdateLogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, update_log: UpdateLog) -> UpdateLog:
        self.session.add(update_log)
        self.session.flush()
        return update_log
