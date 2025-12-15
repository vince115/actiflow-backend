# app/schemas/membership_application/membership_application_response.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.schemas.membership_application.membership_application_base import (
    MembershipApplicationBase
)


class MembershipApplicationResponse(MembershipApplicationBase):
    """
    回傳完整的申請資料（管理後台用）
    """
    application_uuid: str

    user_uuid: UUID
    organizer_uuid: UUID

    # 搭配列表用的可選欄位
    user_name: Optional[str] = None
    organizer_name: Optional[str] = None

    model_config = {"from_attributes": True}
