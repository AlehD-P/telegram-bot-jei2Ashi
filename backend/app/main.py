from __future__ import annotations

from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_miniapp import router as miniapp_router
from app.api.routes_telegram import router as telegram_router
from app.config import get_settings
from app.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title="Telegram Bot Platform")
app.include_router(health_router)
app.include_router(telegram_router)
app.include_router(miniapp_router, prefix="/api")
