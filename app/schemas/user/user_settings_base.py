# app/schemas/user/user_settings.py

from pydantic import BaseModel
from typing import Dict, Any


class UserSettingsBase(BaseModel):
    """
    UserSettings 基底（internal / response 共用）
    """

    settings: Dict[str, Any]

    model_config = {
        "from_attributes": True
    }
