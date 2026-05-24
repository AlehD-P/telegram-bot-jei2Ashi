from __future__ import annotations

from abc import ABC, abstractmethod


class StorageBase(ABC):
    @abstractmethod
    def save(self, key: str, content: bytes) -> None:
        raise NotImplementedError
