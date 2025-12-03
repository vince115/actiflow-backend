# app/crud/submission_value.py

from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy.orm import Session, joinedload

from app.models.submission_value import SubmissionValue
from app.models.event_field import EventField   # ← 必加（驗證 event_field）
from app.schemas.submission_value import (
    SubmissionValueCreate,
    SubmissionValueUpdate
)


# ------------------------------------------------------------
# Create SubmissionValue（後端主導 field_key 與安全驗證）
# ------------------------------------------------------------
def create_submission_value(
    db: Session,
    submission_uuid: str,
    data: SubmissionValueCreate,
    creator_uuid: Optional[str] = None,
    creator_role: str = "user"
) -> SubmissionValue:

    # 取得 EventField → 防止假欄位 ID
    event_field = (
        db.query(EventField)
        .filter(
            EventField.uuid == str(data.event_field_uuid),
            EventField.is_deleted == False
        )
        .first()
    )

    if not event_field:
        raise ValueError("Invalid event_field_uuid")

    value = SubmissionValue(
        submission_uuid=submission_uuid,
        event_field_uuid=data.event_field_uuid,
        field_key=event_field.field_key,        # ← 由後端設定，不從前端來
        value=data.value,
        uploaded_file=data.uploaded_file,

        created_by=creator_uuid,
        created_by_role=creator_role,
    )

    db.add(value)
    db.commit()
    db.refresh(value)
    return value


# ------------------------------------------------------------
# Get single value by UUID
# ------------------------------------------------------------
def get_submission_value(
    db: Session,
    value_uuid: str
) -> Optional[SubmissionValue]:

    return (
        db.query(SubmissionValue)
        .options(joinedload(SubmissionValue.field))
        .filter(
            SubmissionValue.uuid == value_uuid,
            SubmissionValue.is_deleted == False
        )
        .first()
    )


# ------------------------------------------------------------
# List all values of a submission
# ------------------------------------------------------------
def list_submission_values(
    db: Session,
    submission_uuid: str
) -> List[SubmissionValue]:

    return (
        db.query(SubmissionValue)
        .options(joinedload(SubmissionValue.field))
        .filter(
            SubmissionValue.submission_uuid == submission_uuid,
            SubmissionValue.is_deleted == False
        )
        .order_by(SubmissionValue.created_at.asc())
        .all()
    )


# ------------------------------------------------------------
# Update single submission value
# ------------------------------------------------------------
def update_submission_value(
    db: Session,
    value_uuid: str,
    data: SubmissionValueUpdate,
    updater_uuid: Optional[str] = None,
    updater_role: str = "user"
) -> Optional[SubmissionValue]:

    value = get_submission_value(db, value_uuid)
    if not value:
        return None

    # 禁止修改欄位定義與外鍵關聯
    forbidden = {"event_field_uuid", "field_key", "submission_uuid"}

    update_data = data.model_dump(exclude_unset=True)

    for key in forbidden:
        update_data.pop(key, None)

    # 套用可修改欄位
    for key, v in update_data.items():
        setattr(value, key, v)

    value.updated_at = datetime.now(timezone.utc)
    value.updated_by = updater_uuid
    value.updated_by_role = updater_role

    db.commit()
    db.refresh(value)
    return value


# ------------------------------------------------------------
# Soft delete value
# ------------------------------------------------------------
def soft_delete_submission_value(
    db: Session,
    value_uuid: str,
    deleter_uuid: Optional[str],
    deleter_role: str
) -> Optional[SubmissionValue]:

    value = get_submission_value(db, value_uuid)
    if not value:
        return None

    value.is_deleted = True
    value.deleted_at = datetime.now(timezone.utc)
    value.deleted_by = deleter_uuid
    value.deleted_by_role = deleter_role

    db.commit()
    return value
