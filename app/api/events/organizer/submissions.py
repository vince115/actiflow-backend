# app/api/events/organizer/submissions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_organizer_admin

from app.models.submission.submission import Submission
from app.schemas.submission.submission_response import SubmissionResponse
from app.schemas.common.pagination import PaginatedResponse


router = APIRouter(
    prefix="/organizer/{organizer_uuid}/events/{event_uuid}/submissions",
    tags=["Organizer - Submissions"],
)


# -------------------------------------------------------------------
# List submissions of an event (organizer admin)
# -------------------------------------------------------------------
@router.get("", response_model=PaginatedResponse[SubmissionResponse])
def list_event_submissions(
    organizer_uuid: UUID,   # 僅作為 routing，不信任
    event_uuid: UUID,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer Admin / Owner：
    取得某活動的報名資料
    """

    # ⚠️ 核心安全條件：event 必須屬於該 organizer
    query = (
        db.query(Submission)
        .join(Submission.event)
        .filter(
            Submission.event_uuid == event_uuid,
            Submission.is_deleted == False,
            Submission.event.has(organizer_uuid=membership.organizer_uuid),
        )
    )

    total = query.count()
    submissions = (
        query
        .order_by(Submission.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedResponse(
        items=[SubmissionResponse.model_validate(s) for s in submissions],
        total=total,
        page=page,
        page_size=page_size,
    )