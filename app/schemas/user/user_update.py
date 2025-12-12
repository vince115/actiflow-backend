# app/schemas/user/user_update.py

from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
from datetime import date


class UserUpdate(BaseModel):
    """
    更新使用者資料（部分欄位）
    """

    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

    birthday: Optional[date] = None
    address: Optional[Dict[str, Any]] = None
    school: Optional[str] = None
    employment: Optional[str] = None
    job_title: Optional[str] = None
    blood_type: Optional[str] = None

    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    model_config = {"from_attributes": True}
