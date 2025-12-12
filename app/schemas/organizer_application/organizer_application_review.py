# app/schemas/organizer_application/organizer_application_review.py

from pydantic import BaseModel
from typing import Optional


class OrganizerApplicationReview(BaseModel):
    """
    Super Admin 審核 Organizer 建立申請。
    """

    status: str              # approved / rejected
    reason: Optional[str] = None   # 若拒絕可填寫原因

    model_config = {"from_attributes": True}
