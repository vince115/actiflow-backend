# app/schemas/user/user_settings_create.py

from pydantic import BaseModel
from typing import Dict, Any


class UserSettingsCreate(BaseModel):
    """
    建立使用者設定（通常首次登入自動建立）
    """

    settings: Dict[str, Any]
