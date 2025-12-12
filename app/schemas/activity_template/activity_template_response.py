# app/schemas/activity_template/activity_template_response.py

from typing import List
from uuid import UUID

from app.schemas.activity_template.activity_template_base import ActivityTemplateBase
from app.schemas.base.base_model import BaseSchema
from app.schemas.template.template_field_response import TemplateFieldResponse
from app.schemas.activity_type.activity_type_response import ActivityTypeResponse


class ActivityTemplateResponse(ActivityTemplateBase, BaseSchema):
    """
    回傳完整模板資訊：
    - 基本欄位（from Base）
    - BaseSchema（uuid、audit）
    - fields（模板欄位）
    - activity_type（活動類型資訊）
    """

    fields: List[TemplateFieldResponse] = []
    activity_type: ActivityTypeResponse | None = None

    model_config = {"from_attributes": True}
