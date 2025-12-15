# app/crud/event/crud_event.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.event.event import Event
from app.schemas.event.core.event_create import EventCreate
from app.schemas.event.core.event_update import EventUpdate


class CRUDEvent(CRUDBase[Event]):

    # ------------------------------------------------------------
    # Create (with organizer ownership)
    # ------------------------------------------------------------
    def create_event_by_organizer(
        self,
        db: Session,
        data: EventCreate,
        creator_uuid: str,
    ) -> Event:
        obj = data.model_dump()
        obj["created_by"] = creator_uuid
        obj["updated_by"] = creator_uuid

        return super().create(db, obj_in=obj)

    # ------------------------------------------------------------
    # Get by UUID
    # ------------------------------------------------------------
    def get_event_by_uuid(self, db: Session, uuid: str) -> Event:
        return (
            db.query(Event)
            .filter(Event.uuid == uuid, Event.is_deleted == False)
            .first()
        )

    # ------------------------------------------------------------
    # List events under organizer
    # ------------------------------------------------------------
    def list_events_by_organizer(self, db: Session, organizer_uuid: str):
        return (
            db.query(Event)
            .filter(
                Event.organizer_uuid == organizer_uuid,
                Event.is_deleted == False
            )
            .all()
        )

    # ------------------------------------------------------------
    # Update event
    # ------------------------------------------------------------
    def update_event(
        self,
        db: Session,
        event_uuid: str,
        data: EventUpdate,
        updated_by: str
    ):
        event = self.get_event_by_uuid(db, event_uuid)
        if not event:
            return None

        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = updated_by

        return super().update(
            db,
            db_obj=event,
            obj_in=update_data,
        )

    # ------------------------------------------------------------
    # Soft delete
    # ------------------------------------------------------------
    def soft_delete_event(
        self,
        db: Session,
        event_uuid: str,
        deleted_by: str
    ):
        event = self.get_event_by_uuid(db, event_uuid)
        if not event:
            return None

        event.is_deleted = True
        event.deleted_by = deleted_by

        db.commit()
        db.refresh(event)

        return event


# ------------------------------------------------------------
# Instantiate CRUD
# ------------------------------------------------------------
event_crud = CRUDEvent(Event)


# ------------------------------------------------------------
# ⭐ Module-level wrapper functions（供 API import）
# ------------------------------------------------------------

def create_event_by_organizer(db: Session, data: EventCreate, creator_uuid: str):
    return event_crud.create_event_by_organizer(db, data, creator_uuid)


def get_event_by_uuid(db: Session, uuid: str):
    return event_crud.get_event_by_uuid(db, uuid)


def list_events_by_organizer(db: Session, organizer_uuid: str):
    return event_crud.list_events_by_organizer(db, organizer_uuid)


def update_event(db: Session, event_uuid: str, data: EventUpdate, updated_by: str):
    return event_crud.update_event(db, event_uuid, data, updated_by)


def soft_delete_event(db: Session, event_uuid: str, deleted_by: str):
    return event_crud.soft_delete_event(db, event_uuid, deleted_by)
