# app/schemas/organizer/organizer_create.py

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, Dict, Any
from app.schemas.common.address import Address


class OrganizerCreate(BaseModel):
    """
    建立 Organizer 使用的資料（由後台或申請流程自動建立）
    """

    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Address] = None

    website: Optional[HttpUrl] = None
    description: Optional[str] = None

    logo_url: Optional[str] = None
    banner_url: Optional[str] = None

    config: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}