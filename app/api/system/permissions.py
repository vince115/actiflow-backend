# app/api/system/permissions.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/system/permissions",
    tags=["System - Permissions"],
)


@router.get("/me")
def get_my_permissions(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    回傳目前使用者的權限摘要
    （給前端快速判斷 UI 顯示）
    """

    membership = user.system_membership

    if not membership:
        return {
            "role": "guest",
            "permissions": []
        }

    return {
        "role": membership.role,
        "permissions": membership.permissions if hasattr(membership, "permissions") else [],
    }
