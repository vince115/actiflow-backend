# app/api/events/public/submissions.py
# ============================================================
# Public Event Submissions
#
# 職責說明：
# - Public 使用者送出活動報名（建立 Submission / SubmissionValue）
# - 建立 EmailVerification 並發送驗證信
# - Email 驗證完成後，透過 confirm-email API 正式推進狀態
#
# 注意：
# - 本檔案「只有 business command 才能推進 submission.status」
# - Auth Email Verification API 不在此檔案
# ============================================================

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta

from starlette import status

from app.core.db import get_db
from app.core.jwt import decode_access_token
from app.core.config import settings

from app.api.utils.submission_code import generate_submission_code
from app.api.utils.email_sender import send_via_resend
from app.api.utils.email_templates import verification_email_html

from app.models.event.event import Event
from app.models.event.event_field import EventField
from app.models.submission.submission import Submission
from app.models.submission.submission_value import SubmissionValue
from app.models.auth.email_verification import EmailVerification

from app.schemas.submission.submission_public import (
    SubmissionPublicCreate,
    SubmissionPublicCreateResponse,
)
from app.schemas.submission.submission_response import SubmissionResponse

from app.crud.submission.crud_submission import submission_crud
from app.crud.submission.crud_submission_status import assert_status_transition
from app.exceptions.submission import InvalidSubmissionStatusTransition
from app.exceptions.base import ActiFlowBusinessException


router = APIRouter(
    prefix="/public/events",
    tags=["Public Event Submissions"],
)

# ============================================================
# Email 驗證完成後，正式推進 Submission 狀態
# ============================================================

@router.post(
    "/submissions/{submission_uuid}/confirm-email",
)
def confirm_email(
    submission_uuid: UUID,
    db: Session = Depends(get_db),
):
    """
    Public API：Email 驗證完成後，推進 Submission 狀態

    前置條件：
    - EmailVerification 必須存在
    - 且已 verified（is_used / verified_at）

    Note:
    - 本 API 為「流程型 command」
    - 使用 CRUD 僅作為 aggregate resolve，不代表純 CRUD API
    """

    # --------------------------------------------------------
    # 1. Resolve Submission (process context)
    # --------------------------------------------------------
    submission = submission_crud.get_by_uuid(db, submission_uuid)
    if not submission:
        raise ActiFlowBusinessException(
            message="Submission not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # --------------------------------------------------------
    # 2. 確認 Email 已驗證
    # --------------------------------------------------------
    verification = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.ref_type == "submission",
            EmailVerification.ref_uuid == submission.uuid,
            EmailVerification.is_deleted == False,
            EmailVerification.is_used == True,
            EmailVerification.verified_at.isnot(None),
        )
        .order_by(EmailVerification.created_at.desc())
        .first()
    )

    if not verification:
        raise ActiFlowBusinessException(
            message="Email not verified yet",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # --------------------------------------------------------
    # 3. 檢查狀態轉換是否合法（Domain Rule）
    # --------------------------------------------------------
    try:
        assert_status_transition(
            current=submission.status,
            target="email_verified",
        )
    except InvalidSubmissionStatusTransition as e:
        raise ActiFlowBusinessException(
            message=str(e),
            status_code=status.HTTP_409_CONFLICT,
        )

    # --------------------------------------------------------
    # 4. 推進狀態
    # --------------------------------------------------------
    submission.status = "email_verified"
    submission.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(submission)

    return submission


# ============================================================
# 使用者送出活動報名（Public Submission Create）
# ============================================================

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
        raise ActiFlowBusinessException(
            message="Event not found or not available",
            status_code=status.HTTP_404_NOT_FOUND,
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
            raise ActiFlowBusinessException(
                message=f"Invalid field_key: {v.field_key}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        values.append(
            SubmissionValue(
                submission_uuid=submission.uuid,
                event_field_uuid=field.uuid,
                field_key=field.field_key,
                value=v.value,
            )
        )

    db.add_all(values)

    # --------------------------------------------------------
    # 6. commit submission + values
    # --------------------------------------------------------
    db.commit()
    db.refresh(submission)

    # --------------------------------------------------------
    # 7. 建立 EmailVerification + 發送驗證信
    # --------------------------------------------------------
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

    verify_url = f"{settings.FRONTEND_BASE_URL}/verify-email?token={token}"

    html = verification_email_html(verify_url)
    send_via_resend(
        to_email=submission.user_email,
        subject="請驗證你的 Email",
        html=html,
    )

    return submission


# ============================================================
# Mark submission as paid
# ============================================================

@router.post("/submissions/{submission_uuid}/mark-paid")
def mark_submission_paid(
    submission_uuid: UUID,
    db: Session = Depends(get_db),
):
    """
    Mark a submission as paid.

    Lifecycle:
    email_verified → paid
    """

    # ---------------------------------------------------------
    # 1. Fetch submission
    # ---------------------------------------------------------
    submission = submission_crud.get_by_uuid(db, submission_uuid)
    if not submission:
        raise ActiFlowBusinessException(
            message="Submission not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # ---------------------------------------------------------
    # 2. Status transition guard
    # ---------------------------------------------------------
    try:
        assert_status_transition(
            current=submission.status,
            target="paid",
        )
    except InvalidSubmissionStatusTransition as e:
        raise ActiFlowBusinessException(
            message=str(e),
            status_code=status.HTTP_409_CONFLICT,
        )

    # ---------------------------------------------------------
    # 3. Update status
    # ---------------------------------------------------------
    submission.status = "paid"
    db.commit()
    db.refresh(submission)

    return {
        "submission_uuid": str(submission.uuid),
        "status": submission.status,
    }