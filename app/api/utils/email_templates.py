# app/api/utils/email_templates.py

def verification_email_html(verify_url: str) -> str:
    return f"""
    <p>請點擊以下連結完成 Email 驗證：</p>
    <a href="{verify_url}">{verify_url}</a>
    """
