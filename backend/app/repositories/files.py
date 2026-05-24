from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.file_object import FileObject


class FileRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, file_object: FileObject) -> FileObject:
        self.session.add(file_object)
        self.session.flush()
        return file_object
