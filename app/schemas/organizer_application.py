# app/schemas/organizer_application.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrganizerApplicationBase(BaseModel):
    application_uuid: str
    user_uuid: str
    organizer_uuid: str
    status: str
    reason: Optional[str] = None
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewer_uuid: Optional[str] = None
    reviewer_role: Optional[str] = None


class OrganizerApplicationResponse(OrganizerApplicationBase):
    class Config:
        from_attributes = True


class OrganizerApplicationReview(BaseModel):
    status: str  # approved / rejected
    reviewer_uuid: str
    reviewer_role: str
    reason: Optional[str] = None
