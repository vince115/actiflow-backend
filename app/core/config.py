# app/core/config.py ← 全域設定：env、常數

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    # === App Metadata ===
    APP_NAME: str = "ActiFlow Backend"
    VERSION: str = "0.1.0"
    ENV: str = "dev"  # dev / prod / test
    
    # === Database ===
    DATABASE_URL: str = ""
    TEST_DATABASE_URL: str = ""

    # === JWT ===
    JWT_SECRET: str = "change_me_please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    COOKIE_SECURE: bool = False  # HTTPS only

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
    
    @property
    def db_url(self) -> str:
        if self.ENV in ("dev", "test"):
            return self.TEST_DATABASE_URL or self.DATABASE_URL
        return self.DATABASE_URL


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
