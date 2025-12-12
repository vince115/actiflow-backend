# app/crud/event/crud_event.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.event.event import Event
from app.schemas.event.event_create import EventCreate
from app.schemas.event.event_update import EventUpdate


class CRUDEvent(CRUDBase[Event]):

    def create(self, db: Session, data: EventCreate) -> Event:
        return super().create(db, obj_in=data.model_dump())

    def update(
        self,
        db: Session,
        db_obj: Event,
        data: EventUpdate
    ) -> Event:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


event_crud = CRUDEvent(Event)
