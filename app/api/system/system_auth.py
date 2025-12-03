# app/api/system/system_auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_system_admin
from app.schemas.system_membership import (
    SystemMembershipCreate,
    SystemMembershipUpdate,
    SystemMembershipResponse
)
from app.crud.system_membership import (
    create_system_membership,
    update_system_membership,
    soft_delete_system_membership,
    get_system_membership,
    list_system_memberships,
)

router = APIRouter(prefix="/system/memberships", tags=["System Membership"])


# ============================================================
# 建立 Platform-level Role（System Admin 專用）
# ============================================================
@router.post("/", response_model=SystemMembershipResponse)
def create_role(
    data: SystemMembershipCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_system_admin)
):
    """
    建立 user 的 system-level membership
    角色可為：system_admin / support / auditor
    """

    membership = create_system_membership(db, data)
    return membership


# ============================================================
# 更新 Platform-level Role（System Admin 專用）
# ============================================================
@router.put("/{user_uuid}", response_model=SystemMembershipResponse)
def update_role(
    user_uuid: str,
    data: SystemMembershipUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_system_admin)
):
    membership = update_system_membership(db, user_uuid, data)

    if not membership:
        raise HTTPException(404, "System membership not found")

    return membership


# ============================================================
# 刪除（軟刪除）Platform-level Role
# ============================================================
@router.delete("/{user_uuid}")
def delete_role(
    user_uuid: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_system_admin)
):
    membership = soft_delete_system_membership(db, user_uuid)
    if not membership:
        raise HTTPException(404, "System membership not found")

    return {"deleted": True}


# ============================================================
# 取得單一 User 的 Platform Role
# ============================================================
@router.get("/{user_uuid}", response_model=SystemMembershipResponse)
def get_role(
    user_uuid: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_system_admin)
):
    membership = get_system_membership(db, user_uuid)
    if not membership:
        raise HTTPException(404, "System membership not found")

    return membership


# ============================================================
# 列出所有 Platform Role
# ============================================================
@router.get("/", response_model=list[SystemMembershipResponse])
def list_roles(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_system_admin)
):
    return list_system_memberships(db)
