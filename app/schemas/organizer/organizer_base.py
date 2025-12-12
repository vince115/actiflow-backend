# app/schemas/organizer/organizer_base.py

from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional, Dict, Any
from app.schemas.common.address import Address
from app.schemas.common.config import ConfigObject


class OrganizerBase(BaseModel):
    """
    Organizer 基本資料（不包含 uuid 與 audit 欄位）
    """

    status: str = "active"

    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    address: Optional[Address] = None

    website: Optional[HttpUrl] = None
    description: Optional[str] = None

    logo_url: Optional[str] = None
    banner_url: Optional[str] = None

    config: Dict[str, Any] = {}

    model_config = {"from_attributes": True}