# app/schemas/submission/submission_public.py

from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime
from app.schemas.submission.submission_value import SubmissionValuePublic


class SubmissionPublic(BaseModel):
    submission_uuid: UUID
    event_uuid: UUID
    status: str
    submitted_at: datetime | None
    values: List[SubmissionValuePublic] = []

    model_config = {"from_attributes": True}
