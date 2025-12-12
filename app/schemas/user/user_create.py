# app/schemas/user/user_create.py

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class UserCreate(BaseModel):
    """
    建立新使用者（後台 / 註冊共用）
    """
    email: EmailStr
    password: str

    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

    birthday: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    school: Optional[str] = None
    employment: Optional[str] = None
    job_title: Optional[str] = None
    blood_type: Optional[str] = None

    config: Dict[str, Any] = {}
