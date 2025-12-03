# app/crud/event.py

from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


# ------------------------------------------------------------
# Core Creator — 統一建立 Event 的邏輯
# ------------------------------------------------------------
def create_event_core(
    db: Session,
    data: EventCreate,
    actor_uuid: str,
    actor_role: str,
) -> Event:

    event = Event(
        event_code=data.event_code,
        organizer_uuid=data.organizer_uuid,
        activity_template_uuid=data.activity_template_uuid,

        name=data.name,
        description=data.description,

        start_date=data.start_date,
        end_date=data.end_date,
        registration_deadline=data.registration_deadline,

        location=data.location,
        banner_url=data.banner_url,

        config=data.config or {},
        status=data.status or "draft",

        created_by=actor_uuid,
        created_by_role=actor_role,
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    return event


# ------------------------------------------------------------
# Create Event (Organizer owner/admin)
# ------------------------------------------------------------
def create_event_by_organizer(
    db: Session,
    data: EventCreate,
    creator_uuid: str
):
    return create_event_core(db, data, creator_uuid, "organizer_admin")


# ------------------------------------------------------------
# Create Event (Super Admin)
# ------------------------------------------------------------
def create_event_by_super_admin(
    db: Session,
    data: EventCreate,
    admin_uuid: str
):
    return create_event_core(db, data, admin_uuid, "super_admin")


# ------------------------------------------------------------
# Get Event by UUID
# ------------------------------------------------------------
def get_event_by_uuid(db: Session, event_uuid: str) -> Optional[Event]:
    return (
        db.query(Event)
        .filter(Event.uuid == event_uuid, Event.is_deleted == False)
        .first()
    )


# ------------------------------------------------------------
# List events under specific organizer
# ------------------------------------------------------------
def list_events_by_organizer(db: Session, organizer_uuid: str) -> List[Event]:
    return (
        db.query(Event)
        .filter(
            Event.organizer_uuid == organizer_uuid,
            Event.is_deleted == False
        )
        .order_by(Event.created_at.desc())
        .all()
    )

# ------------------------------------------------------------
# List events publicly available
# ------------------------------------------------------------
def list_public_events(db: Session):
    return (
        db.query(Event)
        .filter(
            Event.is_deleted == False,
            Event.is_active == True,
            Event.status == "published",
        )
        .order_by(Event.start_date.asc())
        .all()
    )

# ------------------------------------------------------------
# Update Event
# ------------------------------------------------------------
def update_event(
    db: Session,
    event_uuid: str,
    data: EventUpdate,
    updated_by: Optional[str] = None,
    updated_by_role: str = "organizer_admin",
) -> Optional[Event]:

    event = get_event_by_uuid(db, event_uuid)
    if not event:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # 建議禁止 event_code 修改 → 避免前端亂改業務代號
    if "event_code" in update_data:
        pass
        # update_data.pop("event_code")  # ← 若你想禁止修改就取消註解

    for key, value in update_data.items():
        setattr(event, key, value)

    event.updated_at = datetime.now(timezone.utc)
    event.updated_by = updated_by
    event.updated_by_role = updated_by_role

    db.commit()
    db.refresh(event)
    return event


# ------------------------------------------------------------
# Soft Delete Event
# ------------------------------------------------------------
def soft_delete_event(
    db: Session,
    event_uuid: str,
    deleted_by: Optional[str] = None,
    deleted_by_role: str = "organizer_admin",
) -> Optional[Event]:

    event = get_event_by_uuid(db, event_uuid)
    if not event:
        return None

    event.is_deleted = True
    event.deleted_at = datetime.now(timezone.utc)
    event.deleted_by = deleted_by
    event.deleted_by_role = deleted_by_role

    db.commit()
    return event
