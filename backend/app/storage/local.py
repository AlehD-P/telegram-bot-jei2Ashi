from __future__ import annotations

from pathlib import Path

from app.storage.base import StorageBase


class LocalStorage(StorageBase):
    def __init__(self, base_path: str) -> None:
        self.base_path = Path(base_path)

    def save(self, key: str, content: bytes) -> None:
        path = self.base_path / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
