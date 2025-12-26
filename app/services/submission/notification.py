# app/services/submission/notification.py

from sqlalchemy.orm import Session

from app.models.submission.submission import Submission
from app.api.utils.email_mailer import send_generic_email
from app.api.utils.email_templates import (
    submission_rejected_email,
    submission_reopened_email,
    submission_completed_email,
)
from app.core.config import settings


# ============================================================
# Submission Notification Service
# ============================================================
# 責任：
# - 處理 submission 狀態變更後的 email side effects
# - 不修改狀態
# - 不處理權限
# - 不拋 HTTP exception
# ============================================================

# ============================================================
# Submission Rejected Notification
# ============================================================
def notify_submission_rejected(
    *,
    db: Session,
    submission: Submission,
):
    """
    Notify applicant that submission is rejected.

    使用時機：
    - Organizer reject submission
    """

    if not submission.user_email:
        return

    subject, body = submission_rejected_email(
        project_name=settings.PROJECT_NAME,
        reason=submission.status_reason or "未提供具體原因",
    )

    send_generic_email(
        to_email=submission.user_email,
        subject=subject,
        html=body,
    )

# ============================================================
# Submission Reopened Notification
# ============================================================

def notify_submission_reopened(
    *,
    db: Session,
    submission: Submission,
):
    """
    Notify applicant that submission is reopened.

    使用時機：
    - Organizer reopen submission
    """

    if not submission.user_email:
        return

    subject, body = submission_reopened_email(
        project_name=settings.PROJECT_NAME,
        note=submission.notes or "請登入系統查看最新狀態",
    )

    send_generic_email(
        to_email=submission.user_email,
        subject=subject,
        html=body,
    )


# ============================================================
# Submission Approved Notification
# ============================================================

def notify_submission_completed(
    *,
    db: Session,
    submission: Submission,
):
    """
    Notify applicant that submission is approved (completed).

    使用時機：
    - Organizer approve submission
    """

    if not submission.user_email:
        return

    subject, body = submission_completed_email(
        project_name=settings.PROJECT_NAME,
    )

    send_generic_email(
        to_email=submission.user_email,
        subject=subject,
        html=body,
    )
