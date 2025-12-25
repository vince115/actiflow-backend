# app/api/utils/email_verification_mailer.py

from app.core.config import settings
from app.api.utils.email_sender import send_via_resend
from app.api.utils.email_templates import verification_email_html

def send_verification_email(
    *,
    to_email: str,
    token: str,
):
    verify_url = f"{settings.FRONTEND_BASE_URL}/verify-email?token={token}"

    subject = "請驗證你的 Email"

    html = verification_email_html(
        verify_url=verify_url,
    )

    return send_via_resend(
        to_email=to_email,
        subject=subject,
        html=html,
    )

