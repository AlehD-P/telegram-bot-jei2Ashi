from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "success", "data": {"state": "alive"}}


@router.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "success", "data": {"state": "ready"}}
