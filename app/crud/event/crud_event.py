# app/crud/event/crud_event.py

from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.base.crud_base import CRUDBase
from app.models.event.event import Event

from app.schemas.event.core.event_create import OrganizerEventCreate
from app.schemas.event.core.event_update import EventUpdate
from app.schemas.event.core.event_status_update import EventStatus

from app.crud.activity.crud_activity_template import activity_template_crud

# ============================================================
# CRUD Class（純 DB 存取，無業務邏輯）
# ============================================================
class CRUDEvent(CRUDBase[Event]):

    def create(self, db: Session, obj: dict) -> Event:
        return super().create(db, obj_in=obj)

    def get_event_by_uuid(self, db: Session, uuid: UUID) -> Event | None:
        return (
            db.query(Event)
            .filter(
                Event.uuid == uuid,
                Event.is_deleted == False,
            )
            .first()
        )

    def list_events_by_organizer(self, db: Session, organizer_uuid: UUID):
        """
        回傳 Query（給 API 做 pagination）
        """
        return (
            db.query(Event)
            .filter(
                Event.organizer_uuid == organizer_uuid,
                Event.is_deleted == False,
            )
        )


# ------------------------------------------------------------
# Instantiate CRUD
# ------------------------------------------------------------
event_crud = CRUDEvent(Event)


# ============================================================
# Organizer scoped business logic
# ============================================================
def create_event_by_organizer(
    db: Session,
    organizer_uuid: UUID,
    data: OrganizerEventCreate,
    creator_uuid: UUID,
    creator_role: str,
) -> Event:
    """
    建立 Event（Organizer scoped）
    - 驗證 activity template ownership
    - organizer / audit 欄位由後端注入
    """

    # --------------------------------------------------------
    # 1. 驗證 ActivityTemplate 是否屬於該 organizer
    # --------------------------------------------------------
    template = activity_template_crud.get(db, data.activity_template_uuid)

    if not template or template.organizer_uuid != organizer_uuid:
        #  這裡不丟 HTTPException（API 層處理）
        raise ValueError("Invalid activity template")

    # --------------------------------------------------------
    # 2. 組合建立資料
    # --------------------------------------------------------
    obj = data.model_dump()
    obj.update(
        {
            "organizer_uuid": organizer_uuid,
            "event_code": f"EV-{str(creator_uuid)[:8]}",  # 暫時簡單生成
            "created_by": creator_uuid,
            "created_by_role": creator_role,
        }
    )

    # --------------------------------------------------------
    # 3. 建立 Event
    # --------------------------------------------------------
    return event_crud.create(db, obj)



# ============================================================
# ⭐ Module-level wrapper functions（供 API import）
# ============================================================

def get_event_by_uuid(db: Session, event_uuid: UUID):
    return event_crud.get_event_by_uuid(db, event_uuid)


def list_events_by_organizer(db: Session, organizer_uuid: UUID):
    return event_crud.list_events_by_organizer(db, organizer_uuid)


def update_event_by_organizer(
    db: Session,
    event_uuid: UUID,
    data: EventUpdate,
    updater_uuid: UUID,
    updater_role: str,
):
    event = event_crud.get_event_by_uuid(db, event_uuid)
    if not event or event.is_deleted:
        return None

    update_data = data.model_dump(exclude_unset=True)
    update_data.update(
        {
            "updated_by": updater_uuid,
            "updated_by_role": updater_role,
        }
    )

    return event_crud.update(db, db_obj=event, obj_in=update_data)


def soft_delete_event_by_organizer(
    db: Session,
    event_uuid: UUID,
    deleter_uuid: UUID,
    deleter_role: str,
):
    event = event_crud.get_event_by_uuid(db, event_uuid)
    if not event or event.is_deleted:
        return None

    event.is_deleted = True
    event.deleted_by = deleter_uuid
    event.deleted_by_role = deleter_role

    db.commit()
    db.refresh(event)
    return event


# ============================================================
# ⭐ NEW: update event status (publish / close)
# ============================================================
def update_event_status_by_organizer(
    db: Session,
    event_uuid: UUID,
    new_status: EventStatus,
    updater_uuid: UUID,
    updater_role: str,
):
    event = event_crud.get_event_by_uuid(db, event_uuid)
    if not event or event.is_deleted:
        return None

    event.status = new_status
    event.updated_by = updater_uuid
    event.updated_by_role = updater_role

    db.commit()
    db.refresh(event)
    return event