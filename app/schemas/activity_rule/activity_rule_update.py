# app/schemas/activity_rule/activity_rule_update.py

from pydantic import BaseModel
from typing import Optional, Dict, Any


class ActivityRuleUpdate(BaseModel):
    """
    更新 ActivityRule（部分更新）
    """
    rule_type: Optional[str] = None
    rule_key: Optional[str] = None
    rule_value: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
