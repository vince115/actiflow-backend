# app/api/organizers/admin/organizer_members.py


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.db import get_db
from app.api.organizers.dependencies import require_organizer_admin

from app.schemas.membership.organizer.organizer_membership_create import OrganizerMembershipCreate
from app.schemas.membership.organizer.organizer_membership_update import OrganizerMembershipUpdate
from app.schemas.membership.organizer.organizer_membership_response import OrganizerMembershipResponse

from app.crud.membership.crud_organizer_membership import (
    list_members_by_organizer,
    create_membership,
    update_membership,
    soft_delete_membership,
    set_organizer_owner
)

router = APIRouter(
    prefix="/organizers/members",
    tags=["Organizer Members"],
)

# ------------------------------------------------------------
# Helper：檢查使用者是否為該 Organizer 的 owner/admin
# ------------------------------------------------------------
def assert_organizer_admin(user, organizer_uuid: str):
    """
    檢查 user 是否為該 organizer 的 owner / admin
    """
    if user.role == "system_admin":
        return  # 系統管理員永遠有權限

    # 檢查 membership
    membership = next(
        (m for m in user.organizer_memberships if m.organizer_uuid == organizer_uuid),
        None
    )

    if not membership or membership.role not in ("owner", "admin"):
        raise HTTPException(403, "No permission for this organizer")


# ------------------------------------------------------------
# 1. List members 列出某 Organizer 的所有成員
# ------------------------------------------------------------
@router.get("/", response_model=List[OrganizerMembershipResponse])
def list_members(
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin)
):
    return list_members_by_organizer(db, membership.organizer_uuid)


# ------------------------------------------------------------
# 2. Add member 新增 Organizer 成員
# ------------------------------------------------------------
@router.post("/", response_model=OrganizerMembershipResponse)
def add_member(
    data: OrganizerMembershipCreate,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin)
):
    new_membership = create_membership(
        db=db,
        user_uuid=data.user_uuid,
        organizer_uuid=membership.organizer_uuid,
        role=data.role,
        created_by=membership.user_uuid,
        created_by_role=membership.role,
    )
    return new_membership


# ------------------------------------------------------------
# 3. Update member 更新成員角色（admin → staff、staff → reviewer等）
# ------------------------------------------------------------
@router.put("/{user_uuid}", response_model=OrganizerMembershipResponse)
def update_member(
    user_uuid: UUID,
    data: OrganizerMembershipUpdate,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin),
):
    updated = update_membership(
        db=db,
        user_uuid=user_uuid,
        organizer_uuid=membership.organizer_uuid,
        data=data,
        updated_by=membership.user_uuid,
        updated_by_role=membership.role,
    )
    if not updated:
        raise HTTPException(404, "Membership not found")

    return updated


# ------------------------------------------------------------
# 4. Delete member 移除成員（軟刪除）
# ------------------------------------------------------------
@router.delete("/{user_uuid}")
def delete_member(
    user_uuid: UUID,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin),
):
    deleted = soft_delete_membership(
        db=db,
        user_uuid=user_uuid,
        organizer_uuid=membership.organizer_uuid,
        deleted_by=membership.user_uuid,
        deleted_by_role=membership.role,
    )

    if not deleted:
        raise HTTPException(404, "Membership not found")

    return {"deleted": True}

# ------------------------------------------------------------
# 5. Transfer organizer ownership（最高權限：owner）
# ------------------------------------------------------------
@router.post("/{user_uuid}/transfer-ownership")
def transfer_ownership(
    user_uuid: UUID,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin),
):
    """
    將 Organizer Owner 轉移給指定成員
    - 僅限目前 organizer 的 owner
    """

    # Guard 已確保是 organizer admin / owner
    if membership.role != "owner":
        raise HTTPException(403, "Only owner can transfer ownership")

    success = set_organizer_owner(
        db=db,
        organizer_uuid=membership.organizer_uuid,
        new_owner_user_uuid=user_uuid,
        updated_by=membership.user_uuid,
        updated_by_role=membership.role,
    )

    if not success:
        raise HTTPException(400, "Failed to transfer ownership")

    return {
        "message": "Ownership transferred",
        "organizer_uuid": membership.organizer_uuid,
        "new_owner_user_uuid": user_uuid,
    }
