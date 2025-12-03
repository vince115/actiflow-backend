# app/schemas/event_field.py

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime


# ============================================================
# Base（通用欄位）
# ============================================================
class EventFieldBase(BaseModel):
    field_key: str
    label: str
    field_type: str              # text / email / select / file …
    placeholder: Optional[str] = None
    required: bool = False
    sort_order: int = 0

    options: Optional[List[Any]] = None   # ← 正確：list，不是 dict
    config: Optional[Dict[str, Any]] = None

    # 狀態
    is_active: bool = True
    is_deleted: bool = False

    # Audit fields
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    created_by_role: Optional[str] = None
    updated_by_role: Optional[str] = None
    deleted_by_role: Optional[str] = None



# ============================================================
# Create（body 不能包含 event_uuid！）
# ============================================================
class EventFieldCreate(BaseModel):
    field_key: str
    label: str
    field_type: str

    placeholder: Optional[str] = None
    required: bool = False
    sort_order: int = 0

    options: Optional[List[Any]] = None    # ← list
    config: Optional[Dict[str, Any]] = None

    # audit
    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# ============================================================
# Update
# ============================================================
class EventFieldUpdate(BaseModel):
    label: Optional[str] = None
    placeholder: Optional[str] = None
    field_type: Optional[str] = None
    required: Optional[bool] = None
    sort_order: Optional[int] = None
    options: Optional[List[Any]] = None    # ← list
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None


# ============================================================
# Response
# ============================================================
class EventFieldResponse(EventFieldBase):
    uuid: UUID
    event_uuid: UUID

    class Config:
        from_attributes = True