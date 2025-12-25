# app/api/auth/email_verification.py

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.auth.email_verification import EmailVerification

router = APIRouter(
    prefix="/auth/email-verification",
    tags=["Auth - Email Verification"],
)


@router.get("/verify")
def verify_email(
    token: str = Query(..., description="Email verification token"),
    db: Session = Depends(get_db),
):
    """
    Email 驗證入口（使用者從信件點擊）

    ⚠️ 注意：
    - 此 API 僅負責 email 驗證（gate）
    - 不推進任何業務狀態（submission.status）
    """

    now = datetime.now(timezone.utc)

    # --------------------------------------------------------
    # 1. 查詢驗證紀錄
    # --------------------------------------------------------
    verification = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.token == token,
            EmailVerification.is_deleted == False,
        )
        .first()
    )

    if not verification:
        raise HTTPException(
            status_code=404,
            detail="Invalid or expired verification token",
        )

    # --------------------------------------------------------
    # 2. 狀態檢查
    # --------------------------------------------------------
    if verification.is_used or verification.verified_at is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already verified",
        )

    expires_at = verification.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise HTTPException(
            status_code=400,
            detail="Verification token expired",
        )

    # --------------------------------------------------------
    # 3. 標記 Email 為已驗證
    # --------------------------------------------------------
    verification.is_used = True
    verification.verified_at = now

    db.commit()

    return {
        "status": "verified",
        "ref_type": verification.ref_type,
        "ref_uuid": str(verification.ref_uuid),
    }
