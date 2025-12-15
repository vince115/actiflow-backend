# app/schemas/membership_application/membership_application_base.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class MembershipApplicationBase(BaseModel):
    """
    基本欄位（用於 Response + Internal）
    """
    status: str = "pending"   # pending / approved / rejected
    reason: Optional[str] = None

    submitted_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None

    reviewer_uuid: Optional[UUID] = None
    reviewer_role: Optional[str] = None

    model_config = {"from_attributes": True}
