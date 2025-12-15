# app/schemas/organizer_application/organizer_application_base.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class OrganizerApplicationBase(BaseModel):
    """
    Organizer Application 的核心 Domain Schema
    - 不包含 uuid / audit（由 BaseSchema 負責）
    - 不包含審核者資訊（屬於流程層）
    """

    # 申請人
    user_uuid: UUID

    # 申請建立的 Organizer 資料
    name: str
    description: Optional[str] = None

    # 申請原因（使用者填寫）
    reason: Optional[str] = None

    # Domain 狀態
    # pending / approved / rejected
    status: str = "pending"
