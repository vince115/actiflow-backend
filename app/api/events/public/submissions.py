# app/api/events/public/submissions.py
# 使用者送出報名（Public Submission Create）

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta

from app.api.utils.submission_code import generate_submission_code
from app.api.utils.email_sender import send_via_resend
from app.api.utils.email_templates import verification_email_html

from app.core.db import get_db
from app.core.jwt import decode_access_token
from app.core.config import settings

from app.models.event.event import Event
from app.models.event.event_field import EventField
from app.models.submission.submission import Submission
from app.models.submission.submission_value import SubmissionValue
from app.models.auth.email_verification import EmailVerification

from app.schemas.submission.submission_public import SubmissionPublicCreate, SubmissionPublicCreateResponse
from app.schemas.submission.submission_response import SubmissionResponse

router = APIRouter(
    prefix="/public/events",
    tags=["Public Event Submissions"],
)


@router.post(
    "/{event_uuid}/submissions",
    response_model=SubmissionPublicCreateResponse,
)
def create_submission(
    event_uuid: UUID,
    data: SubmissionPublicCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Public API：使用者送出活動報名

    行為說明：
    - 建立 Submission（主檔）
    - 使用 field_key → event_field_uuid 映射
    - 同一 transaction 內建立 SubmissionValue（子表）
    """

    # --------------------------------------------------------
    # 1. 檢查 Event 是否存在且可報名
    # --------------------------------------------------------
    event = (
        db.query(Event)
        .filter(
            Event.uuid == event_uuid,
            Event.is_deleted == False,
            Event.status == "published",
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found or not available",
        )

    # --------------------------------------------------------
    # 2. 嘗試取得登入使用者（可選）
    # --------------------------------------------------------
    user_uuid = None
    token = request.cookies.get("access_token")
    if token:
        payload = decode_access_token(token)
        user_uuid = payload.get("sub") if payload else None

    # --------------------------------------------------------
    # 3. 建立 Submission（主檔）
    # --------------------------------------------------------
    submission = Submission(
        submission_code=generate_submission_code(event.event_code),
        event_uuid=event_uuid,
        user_uuid=user_uuid,
        user_email=data.user_email,
        status="pending",
        notes=data.notes,
        extra_data=data.extra_data,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    db.add(submission)
    db.flush()  # 取得 submission.uuid

    # --------------------------------------------------------
    # 4. 準備 field_key → EventField 映射
    # --------------------------------------------------------
    fields = (
        db.query(EventField)
        .filter(
            EventField.event_uuid == event_uuid,
            EventField.is_deleted == False,
            EventField.is_enabled == True,
        )
        .all()
    )

    field_map = {f.field_key: f for f in fields}

    # --------------------------------------------------------
    # 5. 建立 SubmissionValue（子表）
    # --------------------------------------------------------
    values: list[SubmissionValue] = []

    for v in data.values:
        field = field_map.get(v.field_key)
        if not field:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid field_key: {v.field_key}",
            )

        values.append(
            SubmissionValue(
                submission_uuid=submission.uuid,
                event_field_uuid=field.uuid,   # ✅ 正確 FK
                field_key=field.field_key,     # ✅ 必填
                value=v.value,                 # JSONB
            )
        )

    db.add_all(values)

    # --------------------------------------------------------
    # 6. commit transaction
    # --------------------------------------------------------
    db.commit()
    db.refresh(submission)


    # ========================================================
    # 7. 建立 EmailVerification + 發送驗證信（就在這裡）
    # ========================================================

    token = uuid4().hex

    verification = EmailVerification(
        ref_type="submission",
        ref_uuid=submission.uuid,
        email=submission.user_email,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
    )

    db.add(verification)
    db.commit()

    verify_url = (
        f"{settings.FRONTEND_BASE_URL}/verify-email"
        f"?token={token}"
    )

    html = verification_email_html(verify_url)
    send_via_resend(
        to_email=submission.user_email,
        subject="請驗證你的 Email",
        html=html,
    )

    # if user and user.is_email_verified:
    # 直接把 submission.status 推進
    # submission.status = "email_verified"
    # else:
    # 建立 EmailVerification + 發信


    return submission
