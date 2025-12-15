# app/crud/activity/crud_activity_type.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.activity.activity_type import ActivityType
from app.schemas.activity_type.activity_type_create import ActivityTypeCreate
from app.schemas.activity_type.activity_type_update import ActivityTypeUpdate


class CRUDActivityType(CRUDBase[ActivityType]):

    def create(
        self,
        db: Session,
        data: ActivityTypeCreate,
    ) -> ActivityType:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def update(
        self,
        db: Session,
        db_obj: ActivityType,
        data: ActivityTypeUpdate,
    ) -> ActivityType:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


activity_type_crud = CRUDActivityType(ActivityType)
