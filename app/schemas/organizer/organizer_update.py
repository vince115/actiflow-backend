# app/schemas/organizer/organizer_update.py

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, Dict, Any
from app.schemas.common.address import Address


class OrganizerUpdate(BaseModel):
    """
    修改 Organizer 資料使用。
    """

    status: Optional[str] = None

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    address: Optional[Address] = None

    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None

    config: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}