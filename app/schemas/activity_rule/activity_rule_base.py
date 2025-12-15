# app/schemas/activity_rule/activity_rule_base.py

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from uuid import UUID


class ActivityRuleBase(BaseModel):
    """
    ActivityRule 核心欄位
    一條活動規則（報名限制、條件、驗證）
    """

    activity_template_uuid: UUID        # FK → ActivityTemplate.uuid
    rule_type: str                      # e.g. "limit", "validation", "visibility"
    rule_key: str                       # e.g. "max_participants"
    rule_value: Dict[str, Any] = Field(default_factory=dict)

    description: Optional[str] = None
    sort_order: int = 100
