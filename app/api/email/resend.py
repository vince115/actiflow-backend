# app/api/email/resend.py

from datetime import datetime, timedelta, timezone
import secrets

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.config import settings
from app.models.auth.email_verification import EmailVerification
from app.models.submission.submission import Submission

from app.api.utils.email_verification_mailer import send_verification_email

router = APIRouter()

# 冷卻時間（秒）
COOLDOWN_SECONDS = 60
# 每小時最多 N 次 resend
MAX_RESEND_PER_HOUR = 5
# 現在時間
now = datetime.now(timezone.utc)

# -------------------------
# Request / Response Schema
# -------------------------

class ResendEmailRequest(BaseModel):
    ref_type: str
    ref_uuid: str


class ResendEmailResponse(BaseModel):
    status: str


# -------------------------
# Resend Verification Email
# -------------------------

@router.post(
    "/resend",
    response_model=ResendEmailResponse,
    summary="Resend email verification",
)
def resend_verification_email(
    data: ResendEmailRequest,
    db: Session = Depends(get_db),
):
    """
    重送 Email 驗證信（Public）

    行為：
    1. 確認 ref 存在
    2. 確認尚未完成驗證
    3. 作廢舊 token
    4. 建立新 token
    5. 重送驗證信
    """

    now = datetime.now(timezone.utc)

    # --------------------------------------------------
    # 1️⃣ 檢查 ref 是否存在（目前只支援 submission）
    # --------------------------------------------------
    if data.ref_type != "submission":
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported ref_type: {data.ref_type}",
        )

    submission = (
        db.query(Submission)
        .filter(
            Submission.uuid == data.ref_uuid,
            Submission.is_deleted == False,
        )
        .first()
    )

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # --------------------------------------------------
    # 2️⃣ 若已驗證，拒絕 resend
    # --------------------------------------------------
    existing_verified = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.ref_type == "submission",
            EmailVerification.ref_uuid == submission.uuid,
            EmailVerification.verified_at.isnot(None),
            EmailVerification.is_deleted == False,
        )
        .first()
    )

    if existing_verified:
        raise HTTPException(
            status_code=400,
            detail="Email already verified",
        )

    # --------------------------------------------------
    # 2️⃣-1 冷卻時間檢查（60 秒）
    # --------------------------------------------------
    latest_ev = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.ref_type == "submission",
            EmailVerification.ref_uuid == submission.uuid,
            EmailVerification.is_deleted == False,
        )
        .order_by(EmailVerification.created_at.desc())
        .first()
    )

    if latest_ev:
        delta = now - latest_ev.created_at
        if delta.total_seconds() < COOLDOWN_SECONDS:
            raise HTTPException(
                status_code=429,
                detail=f"Please wait {int(COOLDOWN_SECONDS - delta.total_seconds())} seconds before resending.",    
            ) 

    # --------------------------------------------------
    # 2️⃣-2 每小時 resend 次數限制
    # --------------------------------------------------
    one_hour_ago = now - timedelta(hours=1)

    resend_count = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.email == submission.user_email,
            EmailVerification.ref_type == "submission",
            EmailVerification.ref_uuid == submission.uuid,
            EmailVerification.created_at >= one_hour_ago,
            EmailVerification.is_deleted == False,
        )
        .count()
    )

    if resend_count >= MAX_RESEND_PER_HOUR:
        raise HTTPException(
            status_code=429,
            detail="Too many verification emails sent. Please try again later.",
        )  

    # --------------------------------------------------
    # 3️⃣ 作廢舊 token
    # --------------------------------------------------
    db.query(EmailVerification).filter(
        EmailVerification.ref_type == "submission",
        EmailVerification.ref_uuid == submission.uuid,
        EmailVerification.is_used == False,
        EmailVerification.is_deleted == False,
    ).update(
        {
            EmailVerification.is_used: True,
        }
    )

    # --------------------------------------------------
    # 4️⃣ 建立新 EmailVerification
    # --------------------------------------------------
    token = secrets.token_hex(16)

    ev = EmailVerification(
        ref_type="submission",
        ref_uuid=submission.uuid,
        email=submission.user_email,
        token=token,
        expires_at=now + timedelta(minutes=30),
        is_used=False,
    )

    db.add(ev)
    db.commit()
    db.refresh(ev)

    # --------------------------------------------------
    # 5️⃣ 發送驗證信
    # --------------------------------------------------
    send_verification_email(
        to_email=submission.user_email,
        token=token,
    )

    return ResendEmailResponse(status="sent")
