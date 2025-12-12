# app/schemas/user/user_base.py

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, Dict, Any
from datetime import date


class UserBase(BaseModel):
    """
    基本 User 資料（Create / Update / Response 均會繼承）
    """

    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

    birthday: Optional[date] = None
    address: Optional[Dict[str, Any]] = None
    school: Optional[str] = None
    employment: Optional[str] = None
    job_title: Optional[str] = None
    blood_type: Optional[str] = None

    class Config:
        from_attributes = True
