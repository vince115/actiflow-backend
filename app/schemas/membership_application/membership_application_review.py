# app/schemas/membership_application/membership_application_review.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class MembershipApplicationReview(BaseModel):
    """
    後台審核申請（PATCH Body）
    """
    status: str  # "approved" 或 "rejected"
    reviewer_uuid: Optional[UUID] = None
    reviewer_role: Optional[str] = None

    # 可選：拒絕理由（核准時不需要）
    reason: Optional[str] = None
