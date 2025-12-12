# app/schemas/organizer_application/organizer_application_base.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class OrganizerApplicationBase(BaseModel):
    """
    使用者申請建立 Organizer 的基本資料。
    （不包含 uuid 與 audit 欄位）
    """

    user_uuid: UUID

    # 將要建立的 Organizer 的資料
    name: str
    description: Optional[str] = None

    # 申請原因（使用者填寫）
    reason: Optional[str] = None

    # 審核狀態
    status: str = "pending"     # pending / approved / rejected

    # 審核欄位（只有後端與 super admin 使用）
    reviewed_at: Optional[datetime] = None
    reviewer_uuid: Optional[UUID] = None
    reviewer_role: Optional[str] = None

    model_config = {"from_attributes": True}
