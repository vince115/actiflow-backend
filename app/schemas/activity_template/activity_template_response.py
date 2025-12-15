# app/schemas/activity_template/activity_template_response.py

from typing import List, Optional
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.activity_template.activity_template_base import ActivityTemplateBase
from app.schemas.activity_template.activity_template_field_response import (
    ActivityTemplateFieldResponse,
)
from app.schemas.activity_type.activity_type_response import ActivityTypeResponse

class ActivityTemplateResponse(BaseSchema, ActivityTemplateBase):
    """
    ActivityTemplate 回傳用 Schema
    """

    fields: List[ActivityTemplateFieldResponse] = []
    activity_type: Optional[ActivityTypeResponse] = None

    model_config = {"from_attributes": True}
