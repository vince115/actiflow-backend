# app/schemas/activity_rule/activity_rule_response.py

from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime


class ActivityRuleResponse(BaseModel):
    uuid: UUID
    activity_template_uuid: UUID

    rule_type: str
    rule_key: str
    rule_value: Dict[str, Any]
    description: Optional[str]

    sort_order: int
    is_active: bool

    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
