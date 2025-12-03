# app/schemas/user.py

from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID

# --- Login ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Base ---
class UserBase(BaseModel):
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

    role: str = "user"
    auth_provider: str = "local"

    is_email_verified: bool = False

    config: Dict[str, Any] = Field(default_factory=dict)

    is_active: bool = True
    is_deleted: bool = False

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    model_config = {"from_attributes": True}

# --- Create ---
class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

    birthday: Optional[date] = None
    address: Optional[Dict[str, Any]] = None
    school: Optional[str] = None
    employment: Optional[str] = None
    job_title: Optional[str] = None
    blood_type: Optional[str] = None

    auth_provider: Optional[str] = "local"
    config: Dict[str, Any] = Field(default_factory=dict)


# --- Update ---
class UserUpdate(BaseModel):
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

    updated_by: Optional[str] = None

    model_config = {"from_attributes": True}

# --- Response ---
class UserResponse(UserBase):
    uuid: UUID   # ✅ 只有在回傳時才暴露 uuid

# --- Login Response ---
class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

    model_config = {"from_attributes": True}