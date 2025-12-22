# app/crud/activity/crud_activity_template.py  

from sqlalchemy.orm import Session
from app.crud.base.crud_base import CRUDBase
from app.models.activity.activity_template import ActivityTemplate
from uuid import UUID

from app.schemas.activity_template.activity_template_create import ActivityTemplateCreate
from app.schemas.activity_template.activity_template_update import ActivityTemplateUpdate


class CRUDActivityTemplate(CRUDBase[ActivityTemplate]):

    def create(self, db: Session, data: ActivityTemplateCreate) -> ActivityTemplate:
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

activity_template_crud = CRUDActivityTemplate(ActivityTemplate)



# ------------------------------------------------------------
# Module-level helper（供其他模組使用）
# ------------------------------------------------------------
def get_activity_template_by_uuid(
    db: Session,
    template_uuid: UUID,
) -> ActivityTemplate | None:
    return (
        db.query(ActivityTemplate)
        .filter(
            ActivityTemplate.uuid == template_uuid,
            ActivityTemplate.is_deleted == False,
        )
        .first()
    )
