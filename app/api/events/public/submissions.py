#   app/api/events/public/submissions.py # 使用者送出報名

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.jwt import decode_access_token

from app.models.event.event import Event
from app.models.submission.submission import Submission

from app.schemas.submission.submission_create import SubmissionCreate
from app.schemas.submission.submission_response import SubmissionResponse

router = APIRouter(
    prefix="/public/events/submissions",
    tags=["Public Event Submissions"],
)

# ============================================================
# Create submission (public)
# ============================================================
@router.post(
    "/{event_uuid}/submissions",
    response_model=SubmissionResponse,
)
def create_submission(
    event_uuid: UUID,
    data: SubmissionCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Public API：
    使用者送出活動報名

    - 不需要 organizer 權限
    - 可匿名 or 已登入
    - event 必須存在且可報名
    """

    # --------------------------------------------------------
    # 1. 檢查 Event 是否存在且可報名
    # --------------------------------------------------------
    event = (
        db.query(Event)
        .filter(
            Event.uuid == event_uuid,
            Event.is_deleted == False,
            Event.status == "published",  # 只允許已發布活動
        )
        .first()
    )

    if not event:
        raise HTTPException(status_code=404, detail="Event not found or not available")

    # --------------------------------------------------------
    # 2. 嘗試取得登入使用者（可選）
    # --------------------------------------------------------
    user_uuid = None
    token = request.cookies.get("access_token")

    if token:
        payload = decode_access_token(token)
        if payload:
            user_uuid = payload.get("sub")

    # --------------------------------------------------------
    # 3. 建立 Submission
    # --------------------------------------------------------
    submission = Submission(
        event_uuid=event_uuid,
        user_uuid=user_uuid,
        user_email=data.user_email,
        status="pending",
        extra_data=data.extra_data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return SubmissionResponse.model_validate(submission)