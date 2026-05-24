from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["miniapp"])


@router.get("/me")
def me() -> dict[str, str]:
    return {"status": "success", "data": {"user": "anonymous"}}


@router.post("/example-action")
def example_action() -> dict[str, str]:
    return {"status": "success", "data": {"result": "ok"}}
