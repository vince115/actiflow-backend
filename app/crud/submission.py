# app/crud/submission.py

import uuid
from fastapi import HTTPException
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlalchemy.orm import Session, joinedload

from app.models.submission import Submission
from app.models.submission_value import SubmissionValue
from app.models.event_field import EventField
from app.models.event import Event

from app.schemas.submission import (
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionStatusUpdate,
)
from app.schemas.submission_value import SubmissionValueUpdate

ALLOWED_STATUS = {"pending", "paid", "canceled", "completed", "waitlist"}


# ------------------------------------------------------------
# Generate submission_code（唯一追蹤碼）
# ------------------------------------------------------------
def generate_submission_code() -> str:
    return f"SUB-{uuid.uuid4().hex[:10].upper()}"


# ------------------------------------------------------------
# Create submission + values
# ------------------------------------------------------------
def create_submission(
    db: Session,
    data: SubmissionCreate,
    creator_uuid: Optional[str] = None,
    creator_role: str = "user"
) -> Submission:

    # Validate status
    if data.status and data.status not in ALLOWED_STATUS:
        raise HTTPException(400, "Invalid submission status")

    # Check event exists
    event = db.query(Event).filter(Event.uuid == str(data.event_uuid)).first()
    if not event:
        raise HTTPException(404, "Event not found")

    # Create main submission
    submission = Submission(
        submission_code=generate_submission_code(),
        event_uuid=data.event_uuid,
        user_email=data.user_email,
        user_uuid=data.user_uuid,
        status=data.status or "pending",
        notes=data.notes,
        extra_data=data.extra_data or {},

        created_by=creator_uuid,
        created_by_role=creator_role,
        is_active=True,
        is_deleted=False,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    # ------------------------------------------------------------
    # Load event fields from Template (template_uuid)
    # ------------------------------------------------------------
    event_fields = {
        str(f.uuid): f
        for f in db.query(EventField)
        .filter(EventField.template_uuid == event.activity_template_uuid)
        .all()
    }

    # Build SubmissionValue
    for value_data in data.values:
        event_field = event_fields.get(str(value_data.event_field_uuid))

        if not event_field:
            raise HTTPException(400, f"Invalid event_field_uuid: {value_data.event_field_uuid}")

        value = SubmissionValue(
            submission_uuid=submission.uuid,
            event_field_uuid=value_data.event_field_uuid,
            field_key=event_field.field_key,
            value=value_data.value,
            uploaded_file=value_data.uploaded_file,

            created_by=creator_uuid,
            created_by_role=creator_role,
        )
        db.add(value)

    db.commit()
    return submission


# ------------------------------------------------------------
# Get submission by UUID
# ------------------------------------------------------------
def get_submission_by_uuid(db: Session, submission_uuid: str) -> Optional[Submission]:
    return (
        db.query(Submission)
        .options(joinedload(Submission.values))
        .filter(
            Submission.uuid == submission_uuid,
            Submission.is_deleted == False
        )
        .first()
    )


# ------------------------------------------------------------
# Get submission by code
# ------------------------------------------------------------
def get_submission_by_code(db: Session, submission_code: str) -> Optional[Submission]:
    return (
        db.query(Submission)
        .options(joinedload(Submission.values))
        .filter(
            Submission.submission_code == submission_code,
            Submission.is_deleted == False
        )
        .first()
    )


# ------------------------------------------------------------
# Assemble values + labels
# ------------------------------------------------------------
def assemble_submission_values_with_label(
    db: Session, submission: Submission
) -> List[Dict[str, Any]]:

    # Find event → template_uuid
    event = db.query(Event).filter(Event.uuid == submission.event_uuid).first()
    if not event:
        return []

    event_fields = {
        str(f.uuid): f
        for f in db.query(EventField)
        .filter(EventField.template_uuid == event.activity_template_uuid)
        .all()
    }

    result = []
    for v in submission.values:
        f = event_fields.get(str(v.event_field_uuid))
        result.append({
            "value_uuid": str(v.uuid),
            "event_field_uuid": str(v.event_field_uuid),
            "field_key": v.field_key,
            "label": f.label if f else None,
            "value": v.value,
            "uploaded_file": v.uploaded_file,
        })

    return result


# ------------------------------------------------------------
# List submissions by event
# ------------------------------------------------------------
def list_submissions_by_event(
    db: Session,
    event_uuid: str,
    status: Optional[str] = None
) -> List[Submission]:

    query = db.query(Submission).filter(
        Submission.event_uuid == str(event_uuid),
        Submission.is_deleted == False
    )

    if status:
        query = query.filter(Submission.status == status)

    return query.order_by(Submission.created_at.desc()).all()


# ------------------------------------------------------------
# List submissions by user
# ------------------------------------------------------------
def list_submissions_by_user(
    db: Session,
    user_uuid: str
) -> List[Submission]:

    return (
        db.query(Submission)
        .filter(
            Submission.user_uuid == str(user_uuid),
            Submission.is_deleted == False
        )
        .order_by(Submission.created_at.desc())
        .all()
    )


# ------------------------------------------------------------
# Update submission (restricted)
# ------------------------------------------------------------
def update_submission(
    db: Session,
    submission_uuid: str,
    data: SubmissionUpdate,
    updater_uuid: str,
    updater_role: str
) -> Optional[Submission]:

    submission = get_submission_by_uuid(db, submission_uuid)
    if not submission:
        return None

    UPDATABLE_FIELDS = {"notes", "extra_data", "status", "status_reason"}

    for key, value in data.model_dump(exclude_unset=True).items():
        if key in UPDATABLE_FIELDS:
            setattr(submission, key, value)

    submission.updated_by = updater_uuid
    submission.updated_by_role = updater_role
    submission.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(submission)
    return submission


# ------------------------------------------------------------
# Update single value
# ------------------------------------------------------------
def update_submission_value(
    db: Session,
    value_uuid: str,
    data: SubmissionValueUpdate,
    updater_uuid: str,
    updater_role: str
):

    value = (
        db.query(SubmissionValue)
        .filter(
            SubmissionValue.uuid == value_uuid,
            SubmissionValue.is_deleted == False
        )
        .first()
    )

    if not value:
        return None

    for key, v in data.model_dump(exclude_unset=True).items():
        setattr(value, key, v)

    value.updated_by = updater_uuid
    value.updated_by_role = updater_role
    value.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(value)
    return value


# ------------------------------------------------------------
# Update submission status only
# ------------------------------------------------------------
def update_submission_status(
    db: Session,
    submission_uuid: str,
    data: SubmissionStatusUpdate,
    updater_uuid: str,
    updater_role: str
):

    if data.status not in ALLOWED_STATUS:
        raise HTTPException(400, "Invalid submission status")

    submission = get_submission_by_uuid(db, submission_uuid)
    if not submission:
        return None

    submission.status = data.status
    submission.status_reason = data.status_reason

    submission.updated_by = updater_uuid
    submission.updated_by_role = updater_role
    submission.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(submission)
    return submission


# ------------------------------------------------------------
# Soft delete submission
# ------------------------------------------------------------
def soft_delete_submission(
    db: Session,
    submission_uuid: str,
    deleter_uuid: str,
    deleter_role: str
):
    submission = get_submission_by_uuid(db, submission_uuid)
    if not submission:
        return None

    submission.is_deleted = True
    submission.deleted_at = datetime.now(timezone.utc)
    submission.deleted_by = deleter_uuid
    submission.deleted_by_role = deleter_role

    db.commit()
    return submission


# ------------------------------------------------------------
# Soft delete submission value
# ------------------------------------------------------------
def soft_delete_submission_value(
    db: Session,
    value_uuid: str,
    deleter_uuid: str,
    deleter_role: str
):
    value = (
        db.query(SubmissionValue)
        .filter(
            SubmissionValue.uuid == value_uuid,
            SubmissionValue.is_deleted == False
        )
        .first()
    )

    if not value:
        return None

    value.is_deleted = True
    value.deleted_at = datetime.now(timezone.utc)
    value.deleted_by = deleter_uuid
    value.deleted_by_role = deleter_role

    db.commit()
    return value
