# app/schemas/activity_template/activity_template_create.py

from app.schemas.activity_template.activity_template_base import ActivityTemplateBase

class ActivityTemplateCreate(ActivityTemplateBase):
    """
    建立 ActivityTemplate

    created_by 由後端透過 current_user 注入
    """
    pass
