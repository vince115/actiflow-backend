from uuid import UUID
from app.schemas.activity_template.activity_template_field_base import (
    ActivityTemplateFieldBase,
)


class ActivityTemplateFieldCreate(ActivityTemplateFieldBase):
    """
    建立 ActivityTemplateField
    """

    template_uuid: UUID
