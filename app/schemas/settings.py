# app/schemas/settings.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class SystemSettingsBase(BaseModel):
    site_name: Optional[str] = None
    logo_url: Optional[str] = None
    support_email: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class SystemSettingsUpdate(SystemSettingsBase):
    """用於 PUT / PATCH API"""
    pass


class SystemSettingsResponse(SystemSettingsBase):
    id: int
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
