from __future__ import annotations

from app.bot.commands import handle_help, handle_start, handle_status, handle_unknown


class Dispatcher:
    def dispatch(self, command: str) -> str:
        match command:
            case "/start":
                return handle_start()
            case "/help":
                return handle_help()
            case "/status":
                return handle_status()
            case _:
                return handle_unknown()
