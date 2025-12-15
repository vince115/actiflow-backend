# app/schemas/submission/submission_base.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class SubmissionBase(BaseModel):
    submission_code: str
    event_uuid: UUID
    user_email: str
    user_uuid: Optional[UUID] = None

    status: str = "pending"
    status_reason: Optional[str] = None
    notes: Optional[str] = None

    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    extra_data: Dict[str, Any] = {}

    is_active: bool = True
    is_deleted: bool = False

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    created_by_role: Optional[str] = None
    updated_by_role: Optional[str] = None
    deleted_by_role: Optional[str] = None

    model_config = {"from_attributes": True}
