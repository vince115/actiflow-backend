# app/api/organizers/organizer_members.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.db import get_db
from app.core.dependencies import (
    get_current_system_admin,
    get_current_organizer_admin,
)

from app.schemas.organizer_membership import (
    OrganizerMembershipCreate,
    OrganizerMembershipUpdate,
    OrganizerMembershipResponse,
)

from app.crud.organizer_membership import (
    list_members_by_organizer,  
    create_membership,
    update_membership,
    soft_delete_membership,
    get_membership,
)

router = APIRouter(
    prefix="/organizers/{organizer_uuid}/members",
    tags=["Organizer Members"],
)

# ============================================================
# 1. 列出某 Organizer 的成員
# ============================================================
@router.get("/{organizer_uuid}/members", response_model=List[OrganizerMembershipResponse])
def list_members(
    organizer_uuid: str,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_organizer_admin(organizer_uuid))  # 只有 owner / admin 可以查看
):
    members = list_members_by_organizer(db, organizer_uuid)
    return members


# ============================================================
# 2. 新增成員（加入 Organizer）
# owner、system_admin 都能新增
# ============================================================
@router.post("/", response_model=OrganizerMembershipResponse)
def add_member(
    organizer_uuid: str,
    data: OrganizerMembershipCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_organizer_admin(organizer_uuid))
):
    """
    - data.user_uuid：加入的 user
    - data.role：成員角色（viewer / editor / admin）
    """

    # 檢查是否已經存在 membership
    exist = get_membership(db, data.user_uuid, organizer_uuid)
    if exist and not exist.is_deleted:
        raise HTTPException(400, "User already a member")

    membership = create_membership(db, {
        "user_uuid": data.user_uuid,
        "organizer_uuid": organizer_uuid,
        "role": data.role,

        "created_by": admin.user_uuid,
        "created_by_role": "organizer_admin",
    })

    return membership


# ============================================================
# 3. 更新成員角色／狀態
# ============================================================
@router.put("/{user_uuid}", response_model=OrganizerMembershipResponse)
def update_member(
    organizer_uuid: str,
    user_uuid: str,
    data: OrganizerMembershipUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_organizer_admin(organizer_uuid))
):

    membership = update_membership(db, user_uuid, organizer_uuid, data)

    if not membership:
        raise HTTPException(404, "Membership not found")

    return membership


# ============================================================
# 4. 移除成員（軟刪除）
# ============================================================
@router.delete("/{user_uuid}")
def delete_member(
    organizer_uuid: str,
    user_uuid: str,
    db: Session = Depends(get_db),
    admin = Depends(get_current_organizer_admin(organizer_uuid))
):

    deleted = soft_delete_membership(
        db,
        user_uuid,
        organizer_uuid,
        deleted_by=admin.user_uuid,
        deleted_by_role="organizer_admin",
    )

    if not deleted:
        raise HTTPException(404, "Membership not found")

    return {"deleted": True}
