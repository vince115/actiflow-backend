#  app/crud/submission/crud_submission_public.py

from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.submission.submission import Submission
from app.models.submission.submission_value import SubmissionValue
from app.models.event.event import Event
from app.schemas.submission.submission_public import SubmissionPublicCreate


# -------------------------------------------------
# Public：建立 Submission（主 + values）
# -------------------------------------------------
def create_public_submission(
    *,
    db: Session,
    event: Event,
    data: SubmissionPublicCreate,
    user_uuid: str | None,
    ip_address: str | None,
    user_agent: str | None,
) -> Submission:
    submission = Submission(
        submission_code=f"SUB-{uuid4().hex[:8]}",
        event_uuid=event.uuid,
        user_uuid=user_uuid,
        user_email=data.user_email,
        status="pending",
        notes=data.notes,
        extra_data=data.extra_data,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    db.add(submission)
    db.flush()  # 拿 submission.uuid

    values = [
        SubmissionValue(
            submission_uuid=submission.uuid,
            field_key=v.field_key,
            field_value=v.field_value,
        )
        for v in data.values
    ]

    db.add_all(values)
    db.commit()
    db.refresh(submission)

    return submission
