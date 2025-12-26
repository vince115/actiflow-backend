# app/api/utils/email_templates.py

# ============================================================
# Verification Email
# ============================================================

def verification_email_html(verify_url: str) -> str:
    return f"""
    <p>請點擊以下連結完成 Email 驗證：</p>
    <a href="{verify_url}">{verify_url}</a>
    """

# ============================================================
# Submission Approved (Completed) Email
# ============================================================

def submission_completed_email(
    *,
    project_name: str,
) -> tuple[str, str]:
    subject = f"【{project_name}】報名已通過確認"

    body = f"""
您好，

恭喜您，您報名的活動已通過主辦單位審核，
報名流程已完成。

活動相關資訊請留意後續通知，
或登入系統查看詳情。

感謝您的參與！
"""
    return subject, body


# ============================================================
# Submission Rejected Email
# ============================================================

def submission_rejected_email(
    *,
    project_name: str,
    reason: str,
) -> tuple[str, str]:
    subject = f"【{project_name}】報名未通過通知"

    body = f"""
您好，

很抱歉通知您，您報名的活動未能通過審核。

原因：
{reason}

若您有任何疑問，請聯絡主辦單位。

謝謝您的理解。
"""
    return subject, body

# ============================================================
# Submission Reopened Email
# ============================================================

def submission_reopened_email(
    *,
    project_name: str,
    note: str,
) -> tuple[str, str]:
    subject = f"【{project_name}】報名已重新開啟"

    body = f"""
您好，

您先前的活動報名已被主辦單位重新開啟。

說明：
{note}

目前狀態：待確認 / 待處理

請登入系統查看詳情。

謝謝。
"""
    return subject, body
