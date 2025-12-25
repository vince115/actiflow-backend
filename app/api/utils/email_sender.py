# app/api/utils/email_sender.py

import httpx
from app.core.config import settings

RESEND_ENDPOINT = "https://api.resend.com/emails"

def send_via_resend(
    *,
    to_email: str,
    subject: str,
    html: str,
):
    """
    最底層 Email 發送器（Resend Adapter）
    - 不知道驗證 / submission / token
    - 不包含任何業務語意
    """
    if not settings.RESEND_API_KEY:
        raise RuntimeError("RESEND_API_KEY not set")
 
    if not settings.RESEND_FROM_EMAIL:
        raise RuntimeError("RESEND_FROM_EMAIL not set")


    payload = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html,
    }

    with httpx.Client(timeout=10) as client:
        res = client.post(
            RESEND_ENDPOINT,
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    if res.status_code >= 400:
        raise RuntimeError(f"Resend error: {res.text}")

    return res.json()
