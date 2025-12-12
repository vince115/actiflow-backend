# app/api/organizers/organizer_events.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_organizer_admin_factory

from app.schemas.event.event import (
    EventCreate,
    EventUpdate,
    EventResponse,
)
from crud.event.event import (
    create_event_by_organizer,
    get_event_by_uuid,
    list_events_by_organizer,
    update_event,
    soft_delete_event,
)


router = APIRouter(prefix="/organizers", tags=["Organizer Events"])


# ============================================================
# Event CRUD (for organizer owner/admin)
# 路徑格式：
# /organizers/{organizer_uuid}/events
# ============================================================


# ------------------------------------------------------------
# 1. Create event
# ------------------------------------------------------------
@router.post("/{organizer_uuid}/events", response_model=EventResponse)
def create_organizer_event(
    organizer_uuid: str,
    data: EventCreate,
    db: Session = Depends(get_db),
    membership=Depends(get_current_organizer_admin_factory()),
):
    """
    只有 organizer（owner/admin）才能新增活動。
    """
    # 安全檢查（避免跨組織代碼攻擊）
    if data.organizer_uuid != organizer_uuid:
        raise HTTPException(400, "organizer_uuid mismatch")

    event = create_event_by_organizer(
        db=db,  
        data=data, 
        creator_uuid=membership.user_uuid)
    return EventResponse.model_validate(event)


# ------------------------------------------------------------
# 2. List events under an organizer
# ------------------------------------------------------------
@router.get("/{organizer_uuid}/events", response_model=list[EventResponse])
def list_organizer_events(
    organizer_uuid: str,
    db: Session = Depends(get_db),
    membership=Depends(get_current_organizer_admin_factory()),
):
    events = list_events_by_organizer(db, organizer_uuid)
    return [EventResponse.model_validate(e) for e in events]


# ------------------------------------------------------------
# 3. Get single event
# ------------------------------------------------------------
@router.get("/{organizer_uuid}/events/{event_uuid}", response_model=EventResponse)
def get_organizer_event(
    organizer_uuid: str,
    event_uuid: str,
    db: Session = Depends(get_db),
    membership=Depends(get_current_organizer_admin_factory()),
):
    event = get_event_by_uuid(db, event_uuid)

    if not event or event.organizer_uuid != organizer_uuid:
        raise HTTPException(status_code=404, detail="Event not found")

    return EventResponse.model_validate(event)


# ------------------------------------------------------------
# 4. Update event
# ------------------------------------------------------------
@router.put("/{organizer_uuid}/events/{event_uuid}", response_model=EventResponse)
def update_organizer_event(
    organizer_uuid: str,
    event_uuid: str,
    data: EventUpdate,
    db: Session = Depends(get_db),
    membership=Depends(get_current_organizer_admin_factory()),
):
    event = get_event_by_uuid(db, event_uuid)
    if not event or event.organizer_uuid != organizer_uuid:
        raise HTTPException(404, "Event not found")

    updated = update_event(
        db,
        event_uuid,
        data,
        updated_by=membership.user_uuid
    )
    return EventResponse.model_validate(updated)


# ------------------------------------------------------------
# 5. Soft delete (disable event)
# ------------------------------------------------------------
@router.delete("/{organizer_uuid}/events/{event_uuid}")
def delete_organizer_event(
    organizer_uuid: str,
    event_uuid: str,
    db: Session = Depends(get_db),
    membership=Depends(get_current_organizer_admin_factory()),
):
    event = get_event_by_uuid(db, event_uuid)
    if not event or event.organizer_uuid != organizer_uuid:
        raise HTTPException(404, "Event not found")

    soft_delete_event(
        db,
        event_uuid,
        deleted_by=membership.user_uuid
    )

    return {"deleted": True}
