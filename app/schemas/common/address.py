# app/schemas/common/address.py

from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    """
    通用地址格式，可給 User / Organizer / Event 等使用。
    """
    country: Optional[str] = "Taiwan"
    city: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    postal_code: Optional[str] = None

    model_config = {"from_attributes": True}
