from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, status

from app.bot.dispatcher import Dispatcher
from app.bot.schemas import TelegramUpdate

router = APIRouter(prefix="/telegram", tags=["telegram"])


def _validate_secret(secret_token: str | None) -> None:
    if not secret_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing webhook secret")


@router.post("/webhook")
def webhook(
    update: TelegramUpdate,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict[str, object]:
    _validate_secret(x_telegram_bot_api_secret_token)
    dispatcher = Dispatcher()
    response_text = dispatcher.dispatch(update)
    return {"status": "success", "data": {"response": response_text}}
