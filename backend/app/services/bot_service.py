from __future__ import annotations

from app.bot.dispatcher import Dispatcher


class BotService:
    def __init__(self) -> None:
        self.dispatcher = Dispatcher()
