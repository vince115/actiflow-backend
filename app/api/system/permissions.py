# app/api/system/permissions.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity

router = APIRouter(
    prefix="/system/permissions",
    tags=["System - Permissions"],
)


@router.get("/me")
def get_my_permissions(
    db: Session = Depends(get_db),
    identity=Depends(get_current_identity),
):
    """
    回傳目前使用者的權限摘要
    （給前端快速判斷 UI 顯示）
    """

    membership = identity.system_membership

    if not membership:
        return {
            "role": "guest",
            "permissions": []
        }

    return {
        "role": membership.role,
        "permissions": membership.permissions if hasattr(membership, "permissions") else [],
    }
