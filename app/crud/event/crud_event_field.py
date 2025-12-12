# app/crud/event/crud_event_field.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.event.event_field import EventField
from app.schemas.event.event_field_create import EventFieldCreate
from app.schemas.event.event_field_update import EventFieldUpdate


class CRUDEventField(CRUDBase[EventField]):

    def create(self, db: Session, data: EventFieldCreate) -> EventField:
        return super().create(db, obj_in=data.model_dump())

    def update(
        self,
        db: Session,
        db_obj: EventField,
        data: EventFieldUpdate
    ) -> EventField:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


event_field_crud = CRUDEventField(EventField)
