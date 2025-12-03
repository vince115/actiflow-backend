# app/crud/activity_type.py

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, List

from app.models.activity_type import ActivityType
from app.schemas.activity_type import (
    ActivityTypeCreate,
    ActivityTypeUpdate,
)


# -----------------------------------------------------------
# Create
# -----------------------------------------------------------
def create_activity_type(
    db: Session,
    data: ActivityTypeCreate,
    creator_uuid: str,
):
    item = ActivityType(
        category_key=data.category_key,
        label=data.label,
        description=data.description,
        color=data.color,
        icon=data.icon,
        sort_order=data.sort_order or 100,
        config=data.config or {},

        created_by=creator_uuid,
        created_by_role=data.created_by_role or "system_admin",
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# -----------------------------------------------------------
# Get single
# -----------------------------------------------------------
def get_activity_type(db: Session, type_uuid: str) -> Optional[ActivityType]:
    return (
        db.query(ActivityType)
        .filter(
            ActivityType.uuid == type_uuid,
            ActivityType.is_deleted == False,
        )
        .first()
    )


# -----------------------------------------------------------
# List all (可選擇是否只列 active)
# -----------------------------------------------------------
def list_activity_types(
    db: Session,
    only_active: bool = False,
) -> List[ActivityType]:

    query = db.query(ActivityType).filter(
        ActivityType.is_deleted == False
    )

    if only_active:
        query = query.filter(ActivityType.is_active == True)

    return query.order_by(ActivityType.sort_order.asc()).all()


# -----------------------------------------------------------
# Update
# -----------------------------------------------------------
def update_activity_type(
    db: Session,
    type_uuid: str,
    data: ActivityTypeUpdate,
    updater_uuid: str,
):
    item = get_activity_type(db, type_uuid)
    if not item:
        return None

    # 動態更新欄位
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    # 稽核欄位
    item.updated_by = updater_uuid
    item.updated_by_role = data.updated_by_role or "system_admin"
    item.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(item)
    return item


# -----------------------------------------------------------
# Soft delete
# -----------------------------------------------------------
def soft_delete_activity_type(
    db: Session,
    type_uuid: str,
    deleter_uuid: str,
):
    item = get_activity_type(db, type_uuid)
    if not item:
        return None

    item.is_deleted = True
    item.deleted_at = datetime.now(timezone.utc)
    item.deleted_by = deleter_uuid
    item.deleted_by_role = "system_admin"

    db.commit()
    return item
