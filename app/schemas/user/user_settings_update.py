# app/schemas/user/user_settings_update.py

from pydantic import BaseModel
from typing import Dict, Any


class UserSettingsUpdate(BaseModel):
    """
    更新使用者設定（PUT /me/settings）
    """

    settings: Dict[str, Any]