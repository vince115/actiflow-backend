# app/schemas/template_field.py

from pydantic import BaseModel, field_validator
from typing import Optional, List, Any
from datetime import datetime

# --------------------
# Base (共用欄位)
# --------------------
class TemplateFieldBase(BaseModel):
    field_key: str
    label: str
    field_type: str                      # text/email/select/date/file...
    required: bool = False
    options: Optional[List[Any]] = None  # e.g., ["A", "B", "C"]
    sort_order: int = 0

    # ------ Validator ------
    @field_validator("field_key")
    def validate_key(cls, v):
        if not v or not v.strip():
            raise ValueError("field_key cannot be empty")
        return v


# --------------------
# Create
# --------------------
class TemplateFieldCreate(TemplateFieldBase):
    template_uuid: str                     # FK to activity_templates.template_uuid


# --------------------
# Update
# --------------------
class TemplateFieldUpdate(BaseModel):
    label: Optional[str] = None
    field_type: Optional[str] = None
    required: Optional[bool] = None
    options: Optional[List[Any]] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


# --------------------
# Response
# --------------------
class TemplateFieldResponse(TemplateFieldBase):
    field_uuid: str
    template_uuid: str

    # audit + system fields
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    class Config:
        from_attributes = True
