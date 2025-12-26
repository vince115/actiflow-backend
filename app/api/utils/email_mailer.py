# app/api/utils/email_mailer.py

from app.api.utils.email_sender import send_via_resend

def send_generic_email(
    *,
    to_email: str,
    subject: str,
    html: str,
):
    """
    通用 Email 發送器
    - 不知道 submission
    - 不知道 verification
    - 只是轉呼叫
    """
    return send_via_resend(
        to_email=to_email,
        subject=subject,
        html=html,
    )
