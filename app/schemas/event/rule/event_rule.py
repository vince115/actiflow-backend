# app/schemas/event/rule/event_rule.py

from typing import Dict, Any
from uuid import UUID

from app.schemas.common.base import BaseSchema


# ------------------------------------------------------------
# Event Rule Response
# ------------------------------------------------------------
class EventRule(BaseSchema):
    event_uuid: UUID

    # 規則定義
    rule_type: str              # capacity / time / eligibility / custom
    rule_key: str               # e.g. max_participants
    rule_value: Any             # e.g. 100 / true / "vip_only"
    rule_config: Dict[str, Any] = {}
