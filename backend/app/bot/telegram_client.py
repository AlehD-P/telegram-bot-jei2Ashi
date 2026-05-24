from __future__ import annotations


class TelegramClient:
    def send_message(self, chat_id: int, text: str) -> None:
        _ = (chat_id, text)
