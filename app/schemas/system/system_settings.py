from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ============================================================
# Base（共用欄位）
# ============================================================
class SystemSettingsBase(BaseModel):
    name: str
    value: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: bool = True


# ============================================================
# Update（更新用）
# ============================================================
class SystemSettingsUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


# ============================================================
# Response（回傳用）
# ============================================================
class SystemSettingsResponse(SystemSettingsBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
