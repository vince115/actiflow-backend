# app/api/organizers/organizer/events_list.py
# Organizer 後台 - Events List（Admin UX 用，Read Model）

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.rbac import require_organizer_role

from app.schemas.event.core.event_list_item import OrganizerEventListItem
from app.models.event.event import Event


router = APIRouter(
    prefix="/events",
    tags=["Organizer - Events"],
)


@router.get(
    "",
    response_model=list[OrganizerEventListItem],
    dependencies=[Depends(require_organizer_role(["owner", "admin"]))],
)
def list_organizer_events(
    organizer_uuid: UUID,
    db: Session = Depends(get_db),
):
    """
    Organizer 後台活動列表（Admin UX）
    - Read only
    - 不做 pagination
    - 不 join submission
    - schema 穩定，給前端列表頁使用
    """

    events = (
        db.query(Event)
        .filter(
            Event.organizer_uuid == organizer_uuid,
            Event.is_deleted == False,
        )
        .order_by(Event.created_at.desc())
        .all()
    )

    items: list[OrganizerEventListItem] = []

    for event in events:
        items.append(
            OrganizerEventListItem(
                uuid=event.uuid,
                event_code=event.event_code,   # ✅ 補齊（若實際欄位不同請對應）
                name=event.name,               # ✅ 用 schema 定義的 name
                status=event.status,
                start_date=event.start_date.date() if event.start_date else None,
                end_date=event.end_date.date() if event.end_date else None,
                # UX 階段先給 0，之後再補真實 count
                # submissions_count=submissions_count,
                submissions_count=0,
            )
        )

    return items
