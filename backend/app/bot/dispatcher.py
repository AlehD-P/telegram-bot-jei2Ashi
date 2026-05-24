from __future__ import annotations

from app.bot.commands import handle_help, handle_start, handle_status, handle_unknown
from app.bot.schemas import TelegramUpdate


class Dispatcher:
    def dispatch(self, update: TelegramUpdate) -> str:
        message = update.message
        command = (message.text or "").strip() if message else ""
        if command.startswith("/"):
            command = command.split()[0]

        match command:
            case "/start":
                return handle_start()
            case "/help":
                return handle_help()
            case "/status":
                return handle_status()
            case _:
                return handle_unknown()
