# app/crud/activity/crud_activity.py

from sqlalchemy.orm import Session
from app.crud.base.crud_base import CRUDBase
from app.models.activity.activity import Activity
from app.schemas.activity.activity_create import ActivityCreate
from app.schemas.activity.activity_update import ActivityUpdate


class CRUDActivity(CRUDBase[Activity]):

    def create(self, db: Session, data: ActivityCreate) -> Activity:
        return super().create(db, obj_in=data.model_dump())

    def update(
        self,
        db: Session,
        db_obj: Activity,
        data: ActivityUpdate
    ) -> Activity:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


activity_crud = CRUDActivity(Activity)
