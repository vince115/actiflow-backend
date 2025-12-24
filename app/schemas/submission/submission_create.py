# app/schemas/submission/submission_create.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.schemas.submission.submission_value import SubmissionValueCreate


class SubmissionCreate(BaseModel):
    event_uuid: UUID
    user_email: EmailStr
    user_uuid: Optional[UUID] = None

    values: List[SubmissionValueCreate]

    status: Optional[str] = "pending"
    notes: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None
