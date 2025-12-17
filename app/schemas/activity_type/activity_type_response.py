# app/schemas/activity_type/activity_type_response.py

from uuid import UUID
from app.schemas.activity_type.activity_type_base import ActivityTypeBase
from app.schemas.common.base import BaseSchema


class ActivityTypeResponse(ActivityTypeBase, BaseSchema):
    """
    Response Schema：
    - 包含 BaseSchema（uuid + 稽核欄位）
    - 包含 ActivityTypeBase（核心欄位）
    """
    model_config = {"from_attributes": True}
