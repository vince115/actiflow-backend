# app/schemas/submission/submission_value.py

from pydantic import BaseModel
from typing import Any, Optional
from uuid import UUID


# ------------------------------------------------------------
# Base (後端 internal / Response 基底)
# ------------------------------------------------------------
class SubmissionValueBase(BaseModel):
    field_uuid: UUID                  # 對應 EventField.uuid
    field_type: str                   # text / number / select / checkbox / date / file ...
    value: Any                        # 真正的欄位值
    uploaded_file: Optional[str] = None  # Upload 類型欄位會用到

    model_config = {"from_attributes": True}


# ------------------------------------------------------------
# Create (前台送出 POST)
# ------------------------------------------------------------
class SubmissionValueCreate(BaseModel):
    field_uuid: UUID
    value: Any = None
    uploaded_file: Optional[str] = None


# ------------------------------------------------------------
# Update (修改已存在的 SubmissionValue)
# ------------------------------------------------------------
class SubmissionValueUpdate(BaseModel):
    value: Optional[Any] = None
    uploaded_file: Optional[str] = None


# ------------------------------------------------------------
# Public (前台 /me/submissions 顯示)
# ------------------------------------------------------------
class SubmissionValuePublic(SubmissionValueBase):
    pass


# ------------------------------------------------------------
# Response (後台使用，帶有 uuid)
# ------------------------------------------------------------
class SubmissionValueResponse(SubmissionValueBase):
    uuid: UUID