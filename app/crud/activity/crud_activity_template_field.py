# app/crud/activity/crud_activity_template_field.py

from sqlalchemy.orm import Session
from app.crud.base.crud_base import CRUDBase
from app.models.activity.activity_template_field import ActivityTemplateField
from app.schemas.activity.activity_template_field_create import ActivityTemplateFieldCreate
from app.schemas.activity.activity_template_field_update import ActivityTemplateFieldUpdate


class CRUDActivityTemplateField(CRUDBase[ActivityTemplateField]):

    def create(
        self,
        db: Session,
        data: ActivityTemplateFieldCreate
    ) -> ActivityTemplateField:
        return super().create(db, obj_in=data.model_dump())

    def update(
        self,
        db: Session,
        db_obj: ActivityTemplateField,
        data: ActivityTemplateFieldUpdate
    ) -> ActivityTemplateField:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


activity_template_field_crud = CRUDActivityTemplateField(ActivityTemplateField)
