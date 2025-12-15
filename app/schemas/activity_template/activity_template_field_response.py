# app/schemas/activity_template/activity_template_field_response.py

from uuid import UUID
from typing import Optional, List, Any

from app.schemas.common.base import BaseSchema
from app.schemas.activity_template.activity_template_field_base import (
    ActivityTemplateFieldBase,
)


class ActivityTemplateFieldResponse(BaseSchema, ActivityTemplateFieldBase):
    """
    ActivityTemplateField 回傳用 Schema
    """

    template_uuid: UUID

    model_config = {"from_attributes": True}
