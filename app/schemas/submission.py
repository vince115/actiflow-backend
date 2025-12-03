# app/schemas/submission.py

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


# ------------------------------------------------------------
# Base model（給 Response 用，不給前端 Update 用）
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# SubmissionValueCreate（報名表欄位值）
# ------------------------------------------------------------
class SubmissionValueCreate(BaseModel):
    event_field_uuid: UUID
    value: Optional[Any] = None
    uploaded_file: Optional[str] = None   # ← 正名


# ------------------------------------------------------------
# Create：建立 submission 用
# ------------------------------------------------------------
class SubmissionCreate(BaseModel):
    event_uuid: UUID
    user_email: str
    user_uuid: Optional[UUID] = None

    values: List[SubmissionValueCreate]

    status: Optional[str] = "pending"
    notes: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# ------------------------------------------------------------
# Update：可修改的欄位（避免前端亂改 event_uuid 等危險欄位）
# ------------------------------------------------------------
class SubmissionUpdate(BaseModel):
    status: Optional[str] = None
    status_reason: Optional[str] = None
    notes: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


# ------------------------------------------------------------
# Status Update：專門只改 status
# ------------------------------------------------------------
class SubmissionStatusUpdate(BaseModel):
    status: str
    status_reason: Optional[str] = None


# ------------------------------------------------------------
# Response：後台查詢用
# ------------------------------------------------------------
class SubmissionResponse(SubmissionBase):
    uuid: UUID

    class Config:
        orm_mode = True
