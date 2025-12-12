# app/schemas/platform/system_settings.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from app.schemas.common.base_model import BaseSchema


class SystemSettingsBase(BaseModel):
    """
    全平台設定，例如：
    - SMTP
    - 支付設定
    - 全域品牌設定
    """

    key: str
    value: Dict[str, Any]

    description: Optional[str] = None

    model_config = {"from_attributes": True}


class SystemSettingsCreate(BaseModel):
    key: str
    value: Dict[str, Any]
    description: Optional[str] = None


class SystemSettingsUpdate(BaseModel):
    value: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class SystemSettingsResponse(SystemSettingsBase, BaseSchema):
    pass
