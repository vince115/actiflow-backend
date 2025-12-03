# app/api/admin/super_admin_tools.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin
from app.crud.user import force_reset_password, disable_user_account

router = APIRouter(
    prefix="/admin/super-tools",
    tags=["Super Admin Tools"]
)

# ---- 1. 強制重置密碼 ----
@router.post("/users/{user_id}/force-reset-password")
def super_reset_password(
    user_id: str,
    db: Session = Depends(get_db),
    current_super_admin = Depends(get_current_super_admin)
):
    """SuperAdmin 強制重設使用者密碼"""
    new_pass = force_reset_password(db, user_id)
    return {
        "message": "Password has been force reset",
        "user_id": user_id
    }


# ---- 2. 強制停用某個帳號 ----
@router.post("/users/{user_id}/disable")
def super_disable_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_super_admin = Depends(get_current_super_admin)
):
    """SuperAdmin 停用某位使用者"""
    ok = disable_user_account(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User disabled", "user_id": user_id}


# ---- 3. 系統維護模式開關（可選）----
@router.post("/system/maintenance/{enabled}")
def toggle_maintenance(
    enabled: bool,
    current_super_admin = Depends(get_current_super_admin)
):
    """
    SuperAdmin 切換維護模式（需要你在 Redis 或 DB 儲存狀態）
    """
    # TODO: set maintenance flag
    return {
        "message": "Maintenance mode updated",
        "enabled": enabled
    }
