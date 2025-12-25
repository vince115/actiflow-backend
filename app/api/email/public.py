# app/api/email/public.py

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.auth.email_verification import EmailVerification
from app.models.submission.submission import Submission

router = APIRouter()


# -------------------------
# Request / Response Schema
# -------------------------

class VerifyEmailRequest(BaseModel):
    token: str


class VerifyEmailResponse(BaseModel):
    status: str
    ref_type: str
    ref_uuid: str


# -------------------------
# Verify Email API
# -------------------------

@router.post(
    "/verify",
    response_model=VerifyEmailResponse,
    summary="Verify email by token",
)
def verify_email(
    data: VerifyEmailRequest,
    db: Session = Depends(get_db),
):
    """
    Email 驗證 API（Public）

    流程：
    1. 依 token 找 email_verifications
    2. 檢查是否存在 / 是否過期 / 是否已使用
    3. 標記為 verified
    4. 依 ref_type 更新對應資料
    """
    
    
    ev = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.token == data.token,
            EmailVerification.is_deleted == False,
        )
        .first()
    )

    if not ev:
        raise HTTPException(status_code=400, detail="Invalid verification token")

    if ev.is_used or ev.verified_at is not None:
        raise HTTPException(
            status_code=400,
            detail="Verification token already used",
        )

    now = datetime.now(timezone.utc)

    expires_at = ev.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise HTTPException(status_code=400, detail="Verification token expired")

    # 標記驗證
    ev.is_used = True
    ev.verified_at = now

    # ref 處理
    if ev.ref_type == "submission":
        submission = (
            db.query(Submission)
            .filter(
                Submission.uuid == ev.ref_uuid,
                Submission.is_deleted == False,
            )
            .first()
        )

        if not submission:
            raise HTTPException(
                status_code=400,
                detail="Related submission not found",
            )
        # Email 已驗證，但 submission 狀態不動
        # submission.status = "email_verified"

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported ref_type: {ev.ref_type}",
        )

    db.commit()

    return VerifyEmailResponse(
        status="verified",
        ref_type=ev.ref_type,
        ref_uuid=str(ev.ref_uuid),
    )
