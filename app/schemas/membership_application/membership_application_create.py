# app/schemas/membership_application/membership_application_create.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class MembershipApplicationCreate(BaseModel):
    """
    User 提交加入組織的申請（POST Body）
    """
    organizer_uuid: UUID
    reason: Optional[str] = None

    # System 自動帶入：user_uuid = current_user.uuid
    # 不需要出現在 schema
