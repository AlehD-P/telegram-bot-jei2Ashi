from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook")
def webhook(update: dict) -> dict[str, str]:
    return {"status": "success", "data": {"received": "true"}}
