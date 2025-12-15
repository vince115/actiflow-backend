# app/crud/event/crud_event_staff.py

from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from app.models.event.event_staff import EventStaff
from app.models.event.event import Event

from app.schemas.event.staff.event_staff_create import EventStaffCreate
from app.schemas.event.staff.event_staff_update import EventStaffUpdate


class EventStaffCRUD:
    """
    EventStaff CRUD
    - 所有操作都必須綁定 organizer_uuid（防止跨 organizer 操作）
    - 僅做資料層邏輯，不處理 RBAC
    """

    # ------------------------------------------------------------
    # Internal helper：確認 Event 屬於該 organizer
    # ------------------------------------------------------------
    def _get_event(
        self,
        db: Session,
        event_uuid: UUID,
        organizer_uuid: UUID,
    ) -> Optional[Event]:
        return (
            db.query(Event)
            .filter(
                Event.uuid == event_uuid,
                Event.organizer_uuid == organizer_uuid,
                Event.is_deleted == False,
            )
            .first()
        )

    # ------------------------------------------------------------
    # List staff by event
    # ------------------------------------------------------------
    def list_by_event(
        self,
        db: Session,
        event_uuid: UUID,
        organizer_uuid: UUID,
    ) -> List[EventStaff]:
        event = self._get_event(db, event_uuid, organizer_uuid)
        if not event:
            return []

        return (
            db.query(EventStaff)
            .filter(
                EventStaff.event_uuid == event_uuid,
                EventStaff.is_deleted == False,
            )
            .order_by(EventStaff.created_at.asc())
            .all()
        )

    # ------------------------------------------------------------
    # Create staff
    # ------------------------------------------------------------
    def create(
        self,
        db: Session,
        event_uuid: UUID,
        organizer_uuid: UUID,
        data: EventStaffCreate,
        created_by: UUID,
        created_by_role: str,
    ) -> Optional[EventStaff]:
        event = self._get_event(db, event_uuid, organizer_uuid)
        if not event:
            return None

        staff = EventStaff(
            event_uuid=event_uuid,
            **data.model_dump(),
        )

        staff.created_by = created_by
        staff.created_by_role = created_by_role

        db.add(staff)
        db.commit()
        db.refresh(staff)

        return staff

    # ------------------------------------------------------------
    # Update staff
    # ------------------------------------------------------------
    def update(
        self,
        db: Session,
        event_uuid: UUID,
        staff_uuid: UUID,
        organizer_uuid: UUID,
        data: EventStaffUpdate,
        updated_by: UUID,
        updated_by_role: str,
    ) -> Optional[EventStaff]:
        event = self._get_event(db, event_uuid, organizer_uuid)
        if not event:
            return None

        staff = (
            db.query(EventStaff)
            .filter(
                EventStaff.uuid == staff_uuid,
                EventStaff.event_uuid == event_uuid,
                EventStaff.is_deleted == False,
            )
            .first()
        )

        if not staff:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(staff, key, value)

        staff.updated_by = updated_by
        staff.updated_by_role = updated_by_role

        db.commit()
        db.refresh(staff)

        return staff

    # ------------------------------------------------------------
    # Soft delete staff
    # ------------------------------------------------------------
    def soft_delete(
        self,
        db: Session,
        event_uuid: UUID,
        staff_uuid: UUID,
        organizer_uuid: UUID,
        deleted_by: UUID,
        deleted_by_role: str,
    ) -> bool:
        event = self._get_event(db, event_uuid, organizer_uuid)
        if not event:
            return False

        staff = (
            db.query(EventStaff)
            .filter(
                EventStaff.uuid == staff_uuid,
                EventStaff.event_uuid == event_uuid,
                EventStaff.is_deleted == False,
            )
            .first()
        )

        if not staff:
            return False

        staff.is_deleted = True
        staff.deleted_by = deleted_by
        staff.deleted_by_role = deleted_by_role

        db.commit()
        return True


# ------------------------------------------------------------
# Singleton
# ------------------------------------------------------------
event_staff_crud = EventStaffCRUD()
