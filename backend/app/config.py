from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

AppEnv = Literal["development", "testing", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: AppEnv = Field(default="development", alias="APP_ENV")
    app_public_base_url: str = Field(default="http://localhost:8000", alias="APP_PUBLIC_BASE_URL")
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    bot_webhook_secret: str = Field(default="", alias="BOT_WEBHOOK_SECRET")
    database_url: str = Field(default="sqlite+pysqlite:///./telegram_bot.db", alias="DATABASE_URL")
    frontend_public_url: str = Field(default="http://localhost:5173", alias="FRONTEND_PUBLIC_URL")
    file_storage_provider: str = Field(default="local", alias="FILE_STORAGE_PROVIDER")
    local_file_storage_path: str = Field(default="./storage", alias="LOCAL_FILE_STORAGE_PATH")
    aws_region: str = Field(default="", alias="AWS_REGION")
    s3_bucket: str = Field(default="", alias="S3_BUCKET")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @field_validator("app_public_base_url", "frontend_public_url")
    @classmethod
    def _strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")

    @field_validator("file_storage_provider")
    @classmethod
    def _validate_storage_provider(cls, value: str) -> str:
        allowed = {"local", "s3"}
        if value not in allowed:
            raise ValueError(f"file_storage_provider must be one of {sorted(allowed)}")
        return value

    @field_validator("bot_token", "bot_webhook_secret", "database_url", "frontend_public_url")
    @classmethod
    def _ensure_required_in_production(cls, value: str, info):
        settings = info.data
        if settings.get("APP_ENV") == "production" and not value:
            raise ValueError(f"{info.field_name} is required in production")
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
