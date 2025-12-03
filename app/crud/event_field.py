from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from app.models.event_field import EventField
from app.schemas.event_field import EventFieldCreate, EventFieldUpdate


# ------------------------------------------------------------
# Create Event Field
# ------------------------------------------------------------
def create_event_field(
    db: Session,
    event_uuid: str,
    data: EventFieldCreate,
    created_by: Optional[str],
    created_by_role: Optional[str]
) -> EventField:

    field = EventField(
        event_uuid=event_uuid,
        field_key=data.field_key,
        label=data.label,
        field_type=data.field_type,
        placeholder=data.placeholder,
        required=data.required,
        sort_order=data.sort_order,

        # 避免 None 覆蓋 default
        options=data.options or [],
        config=data.config or {},

        created_by=created_by,
        created_by_role=created_by_role,
    )

    db.add(field)
    db.commit()
    db.refresh(field)
    return field


# ------------------------------------------------------------
# List fields of event
# ------------------------------------------------------------
def list_event_fields(db: Session, event_uuid: str) -> List[EventField]:
    return (
        db.query(EventField)
        .filter(
            EventField.event_uuid == event_uuid,
            EventField.is_deleted == False,
        )
        .order_by(EventField.sort_order.asc())
        .all()
    )


# ------------------------------------------------------------
# Get field by UUID (PK)
# ------------------------------------------------------------
def get_event_field_by_uuid(db: Session, field_uuid: str) -> Optional[EventField]:
    try:
        field_uuid = UUID(field_uuid)
    except:
        return None

    return (
        db.query(EventField)
        .filter(
            EventField.uuid == field_uuid,       # ← 修正
            EventField.is_deleted == False,
        )
        .first()
    )


# ------------------------------------------------------------
# Update event field
# ------------------------------------------------------------
def update_event_field(
    db: Session,
    field_uuid: str,
    data: EventFieldUpdate,
    updated_by: Optional[str],
    updated_by_role: Optional[str]
) -> Optional[EventField]:

    field = get_event_field_by_uuid(db, field_uuid)
    if not field:
        return None

    # 禁止修改的欄位（保持業務一致性）
    forbidden = {"event_uuid", "field_key"}

    update_data = data.model_dump(exclude_unset=True)
    for key in forbidden:
        update_data.pop(key, None)

    # 套用更新
    for key, val in update_data.items():
        setattr(field, key, val)

    field.updated_at = datetime.now(timezone.utc)
    field.updated_by = updated_by
    field.updated_by_role = updated_by_role

    db.commit()
    db.refresh(field)
    return field


# ------------------------------------------------------------
# Soft delete event field
# ------------------------------------------------------------
def soft_delete_event_field(
    db: Session,
    field_uuid: str,
    deleter_uuid: str,
    deleter_role: str
):
    field = get_event_field_by_uuid(db, field_uuid)
    if not field:
        return None

    field.is_deleted = True
    field.deleted_at = datetime.now(timezone.utc)
    field.deleted_by = deleter_uuid
    field.deleted_by_role = deleter_role

    db.commit()
    return field
