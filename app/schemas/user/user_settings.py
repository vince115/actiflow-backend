# app/schemas/user/user_settings.py

from pydantic import BaseModel
from typing import Optional, Dict, Any


class UserSettingsResponse(BaseModel):
    """
    UserSettings 回傳用（例如 /auth/me）
    """

    preferences: Dict[str, Any] = {}
    notification: Dict[str, Any] = {}

    class Config:
        from_attributes = True
