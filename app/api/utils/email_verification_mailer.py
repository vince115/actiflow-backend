# app/api/utils/email_verification_mailer.py

from app.api.utils.email import send_email


def send_verification_email(
    *,
    to_email: str,
    verify_url: str,
):
    subject = "請驗證你的 Email"

    html = f"""
    <p>您好，</p>
    <p>請點擊以下連結完成 Email 驗證：</p>
    <p>
        <a href="{verify_url}">
            {verify_url}
        </a>
    </p>
    <p>此連結將於 30 分鐘後失效。</p>
    """

    return send_email(
        to=to_email,
        subject=subject,
        html=html,
    )
