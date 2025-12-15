# app/schemas/submission/submission_update.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

# DRAFT / SUBMITTED      → user actions
# PENDING / APPROVED    → review actions
# REJECTED / CANCELLED  → terminal states
# DELETED               → system state


class SubmissionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    DELETED = "deleted"


class SubmissionUpdate(BaseModel):
    status: Optional[SubmissionStatus] = None
    status_reason: Optional[str] = None
    notes: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


class SubmissionStatusUpdate(BaseModel):
    status: SubmissionStatus
    status_reason: Optional[str] = None
