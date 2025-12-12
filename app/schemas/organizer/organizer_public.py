# app/schemas/organizer/organizer_public.py

from pydantic import BaseModel, HttpUrl
from typing import Optional
from uuid import UUID
from app.schemas.common.address import Address


class OrganizerPublic(BaseModel):
    """
    前台顯示專用的 Organizer 精簡資料。
    不包含 email、audit 欄位等敏感資訊。
    """

    uuid: UUID
    name: str
    description: Optional[str] = None

    logo_url: Optional[HttpUrl] = None
    banner_url: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    address: Optional[Address] = None

    model_config = {"from_attributes": True}
