# app/api/events/organizer/submissions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from starlette import status

from app.core.db import get_db
from app.core.dependencies import require_organizer_admin

from app.models.submission.submission import Submission
from app.schemas.submission.submission_response import SubmissionResponse
from app.schemas.common.pagination import PaginatedResponse

from app.crud.submission.crud_submission import submission_crud
from app.crud.submission.crud_submission_status import assert_status_transition

from app.exceptions.base import ActiFlowBusinessException

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


# -------------------------------------------------------------------
# Approve submission (paid -> completed)
# -------------------------------------------------------------------
@router.post("/{submission_uuid}/approve")
def approve_submission(
    organizer_uuid: UUID,   # 僅 routing，不信任
    event_uuid: UUID,
    submission_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer Admin / Owner：
    審核報名（paid -> completed）
    """

    # --------------------------------------------------------
    # 1. 取得 Submission（統一使用 CRUD）
    # --------------------------------------------------------
    submission = submission_crud.get_by_uuid(db, submission_uuid)
    if not submission:
        raise ActiFlowBusinessException(
            message="Submission not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # --------------------------------------------------------
    # 2. 核心安全條件（submission 必須屬於該 event）
    # --------------------------------------------------------
    if submission.event_uuid != event_uuid:
        raise ActiFlowBusinessException(
            message="Submission does not belong to this event",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # --------------------------------------------------------
    # 3. 狀態轉換檢查（domain rule）
    # --------------------------------------------------------
    try:
        assert_status_transition(
            current=submission.status,
            target="completed",
        )
    except Exception as e:
        raise ActiFlowBusinessException(
            message=str(e),
            status_code=status.HTTP_409_CONFLICT,
        )

    # --------------------------------------------------------
    # 4. 推進狀態
    # --------------------------------------------------------
    submission.status = "completed"

    db.commit()
    db.refresh(submission)

    # --------------------------------------------------------
    # 5. Command-style response
    # --------------------------------------------------------
    return {
        "submission_uuid": str(submission.uuid),
        "status": submission.status,
    }