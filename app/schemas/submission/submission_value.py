# app/schemas/submission/submission_value.py

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


# --- Base (給 response 用) ---
class SubmissionValueBase(BaseModel):
    uuid: str                    # 來自 BaseModel
    submission_uuid: str
    event_field_uuid: str
    field_key: str
    value: Any = None
    uploaded_file: Optional[str] = None

    # --- 狀態欄位 ---
    is_active: bool = True            # ★ 新增（企業級系統必要欄位）
    is_deleted: bool = False

    # --- 稽核欄位 ---
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    created_by_role: Optional[str] = None
    updated_by_role: Optional[str] = None
    deleted_by_role: Optional[str] = None


# --- 建立 SubmissionValue ---
class SubmissionValueCreate(BaseModel):
    event_field_uuid: str 
    field_key: str 
    value: Optional[Any] = None 
    file_url: Optional[str] = None

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# --- 修改 SubmissionValue ---
class SubmissionValueUpdate(BaseModel):
    value: Optional[Any] = None
    uploaded_file: Optional[str] = None
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None


# --- 回傳 SubmissionValue ---
class SubmissionValueResponse(SubmissionValueBase):
    class Config:
        from_attributes = True
