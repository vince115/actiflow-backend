from pydantic import BaseModel, field_validator
from typing import Optional, List, Any


class ActivityTemplateFieldBase(BaseModel):
    """
    ActivityTemplateField 的核心欄位
    給 Create / Update / Response 共用
    """

    field_key: str
    label: str
    field_type: str            # text / email / select / date / file
    required: bool = False
    options: Optional[List[Any]] = None
    sort_order: int = 0

    @field_validator("field_key")
    def validate_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("field_key cannot be empty")
        return v.strip()
