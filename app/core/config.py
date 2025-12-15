# app/core/config.py ← 全域設定：env、常數

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    # === App Metadata ===
    APP_NAME: str = "ActiFlow Backend"
    VERSION: str = "0.1.0"
    ENV: str = "dev"  # dev / prod / staging

    # === JWT ===
    JWT_SECRET: str = "change_me_please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # === Database ===
    DATABASE_URL: str = ""

    # === CORS ===
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def split_cors(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # ⭐ pydantic-settings v2 的設定寫法
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
