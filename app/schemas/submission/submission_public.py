# app/schemas/submission/submission_public.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from app.schemas.submission.submission_value import (
    SubmissionValuePublic,
    SubmissionValuePublicCreate,
)

# ============================================================
# Public Create（送出報名表單）
# ============================================================
class SubmissionPublicCreate(BaseModel):
    """
    Public Submission Create 用 schema

    設計說明：
    - 僅允許 public 使用者送出
    - 不暴露 field_uuid
    - 不包含 status / created_by / role
    """

    user_email: EmailStr
    values: List[SubmissionValuePublicCreate]

    notes: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


# ============================================================
# Public Read（查詢 / 顯示）
# ============================================================
class SubmissionPublic(BaseModel):
    submission_uuid: UUID
    event_uuid: UUID
    status: str
    submitted_at: datetime | None
    values: List[SubmissionValuePublic] = []

    model_config = {"from_attributes": True}

# ============================================================
# Public Create Response（送出後立即回傳）
# ============================================================
class SubmissionPublicCreateResponse(BaseModel):
    """
    Public Submission Create Response

    設計說明：
    - 僅回傳建立完成後「一定存在」的欄位
    - 不回傳 values（避免 JOIN / field_type 問題）
    """

    uuid: UUID
    submission_code: str
    status: str

    model_config = {"from_attributes": True}