# app/crud/event/crud_activity_template.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.activity.activity_template import ActivityTemplate
from app.schemas.activity.activity_template_create import ActivityTemplateCreate
from app.schemas.activity.activity_template_update import ActivityTemplateUpdate


class CRUDEventActivityTemplate(CRUDBase[ActivityTemplate]):

    def create(
        self,
        db: Session,
        data: ActivityTemplateCreate
    ) -> ActivityTemplate:
        return super().create(db, obj_in=data.model_dump())

    def update(
        self,
        db: Session,
        db_obj: ActivityTemplate,
        data: ActivityTemplateUpdate
    ) -> ActivityTemplate:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


event_activity_template_crud = CRUDEventActivityTemplate(ActivityTemplate)
