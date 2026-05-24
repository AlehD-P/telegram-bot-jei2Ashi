from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.session import SessionLocal
from app.services.miniapp_auth_service import MiniAppAuthService
from app.services.user_service import UserService

router = APIRouter(tags=["miniapp"])


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_service() -> MiniAppAuthService:
    return MiniAppAuthService()


@router.get("/me")
def me(
    init_data: str | None = Header(default=None, alias="X-Telegram-Init-Data"),
    db: Session = Depends(get_db),
    auth_service: MiniAppAuthService = Depends(get_auth_service),
) -> dict[str, object]:
    if not init_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication data")

    identity = auth_service.validate(init_data)
    user = UserService(db).get_or_create_user(identity.telegram_user_id, identity.username)
    return {"status": "success", "data": {"telegram_user_id": user.telegram_user_id, "username": user.username}}


@router.post("/example-action")
def example_action(
    init_data: str | None = Header(default=None, alias="X-Telegram-Init-Data"),
    auth_service: MiniAppAuthService = Depends(get_auth_service),
) -> dict[str, object]:
    if not init_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication data")

    auth_service.validate(init_data)
    return {"status": "success", "data": {"result": "ok"}}
