# app/api/events/organizer/submissions.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
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

from app.services.submission.notification import notify_submission_rejected, notify_submission_reopened, notify_submission_completed
import logging

from app.exceptions.base import ActiFlowBusinessException

router = APIRouter(
    prefix="/organizer/{organizer_uuid}/events/{event_uuid}/submissions",
    tags=["Organizer - Submissions"],
)
logger = logging.getLogger("submission.commands")

class SubmissionReasonPayload(BaseModel):
    reason: str = Field(..., min_length=1, max_length=500)

# -------------------------------------------------------------------
# A. 取得活動報名資料  List submissions of an event (organizer admin)
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
# B. 審核通過  Approve submission (paid -> completed)
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
    # 5. Email notification (side effect)
    # --------------------------------------------------------
    try:
        notify_submission_completed(
            db=db,
            submission=submission,
        )
    except Exception:
        logger.exception(
            f"Failed to send approval email for submission {submission.uuid}"
        )

    # --------------------------------------------------------
    # 6. Command-style response
    # --------------------------------------------------------
    return {
        "submission_uuid": str(submission.uuid),
        "status": submission.status,
    }


# -------------------------------------------------------------------
# C. 審核不通過   Reject submission (paid -> rejected)
# -------------------------------------------------------------------
@router.post("/{submission_uuid}/reject")
def reject_submission(
    organizer_uuid: UUID,   # routing only
    event_uuid: UUID,
    submission_uuid: UUID,
    payload: SubmissionReasonPayload,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer Admin / Owner：
    拒絕報名（paid -> rejected）
    """

    # --------------------------------------------------------
    # 1. 取得 Submission
    # --------------------------------------------------------
    submission = submission_crud.get_by_uuid(db, submission_uuid)
    if not submission:
        raise ActiFlowBusinessException(
            message="Submission not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # --------------------------------------------------------
    # 2. 核心安全條件
    # --------------------------------------------------------
    if submission.event_uuid != event_uuid:
        raise ActiFlowBusinessException(
            message="Submission does not belong to this event",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # --------------------------------------------------------
    # 3. 狀態轉換檢查（domain）
    # --------------------------------------------------------
    try:
        assert_status_transition(
            current=submission.status,
            target="rejected",
        )
    except Exception as e:
        raise ActiFlowBusinessException(
            message=str(e),
            status_code=status.HTTP_409_CONFLICT,
        )

    # --------------------------------------------------------
    # 4. 推進狀態
    # --------------------------------------------------------
    submission.status = "rejected"
    submission.status_reason = payload.reason
    submission.notes = None

    db.commit()
    db.refresh(submission)

    # --------------------------------------------------------
    # 5. Side effect: email notification (non-blocking)
    # --------------------------------------------------------
    try:
        notify_submission_rejected(
            db=db,
            submission=submission,
        )
    except Exception:
        logger.exception(
            f"Failed to send rejection email for submission {submission.uuid}"
        )

    # --------------------------------------------------------
    # 6. Command-style response
    # --------------------------------------------------------
    return {
        "submission_uuid": str(submission.uuid),
        "status": submission.status,
        "notes": submission.notes,
        "status_reason": submission.status_reason,
    }

# -------------------------------------------------------------------
# D. 重新開啟報名  Reopen submission (completed / rejected -> paid)
# -------------------------------------------------------------------
@router.post("/{submission_uuid}/reopen")
def reopen_submission(
    organizer_uuid: UUID,   # routing only
    event_uuid: UUID,
    submission_uuid: UUID,
    payload: SubmissionReasonPayload,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer Admin / Owner：
    重新開啟報名（completed / rejected -> paid）

    使用情境：
    - 誤審
    - 申請人補資料
    """

    # --------------------------------------------------------
    # 1. 取得 Submission
    # --------------------------------------------------------
    submission = submission_crud.get_by_uuid(db, submission_uuid)
    if not submission:
        raise ActiFlowBusinessException(
            message="Submission not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # --------------------------------------------------------
    # 2. 核心安全條件（必須屬於該 event）
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
            target="paid",
        )
    except Exception as e:
        raise ActiFlowBusinessException(
            message=str(e),
            status_code=status.HTTP_409_CONFLICT,
        )

    # --------------------------------------------------------
    # 4. 推進狀態
    # --------------------------------------------------------
    # status_reason = 對「使用者 / 外部」的官方理由（reject）
    # notes         = 對「內部 / organizer / admin」的操作備註（reopen）
    # --------------------------------------------------------
    submission.status = "paid"
    submission.status_reason = None
    submission.notes = payload.reason

    db.commit()
    db.refresh(submission)

    # --------------------------------------------------------
    # 5. Side effect: email notification (non-blocking)
    # --------------------------------------------------------
    try:
        notify_submission_reopened(
            db=db,
            submission=submission,
        )
    except Exception:
        logger.exception(
            f"Failed to send reopen email for submission {submission.uuid}"
        )

    # --------------------------------------------------------
    # 6. Command-style response
    # --------------------------------------------------------
    return {
        "submission_uuid": str(submission.uuid),
        "status": submission.status,
        "notes": submission.notes,
        "status_reason": submission.status_reason,
    }
