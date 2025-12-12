# app/schemas/template/template_field_base.py

from pydantic import BaseModel, field_validator
from typing import Optional, List, Any


class TemplateFieldBase(BaseModel):
    """
    TemplateField 的核心欄位（不含 uuid / audit）。
    給 Create / Update / Response 共用。
    """

    field_key: str                         # 唯一欄位 key（例如: name / email）
    label: str                             # 顯示標籤
    field_type: str                        # text / email / select / date / file ...
    required: bool = False
    options: Optional[List[Any]] = None    # e.g. ["A", "B", "C"]
    sort_order: int = 0                    # 欄位排序

    @field_validator("field_key")
    def validate_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("field_key cannot be empty")
        return v
