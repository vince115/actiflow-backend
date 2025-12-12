# app/api/organizers/organizer_members.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.db import get_db
from app.core.dependencies import get_current_user  # ★ 新版 Auth

from app.schemas.membership.organizer_membership import (
    OrganizerMembershipCreate,
    OrganizerMembershipUpdate,
    OrganizerMembershipResponse,
)

from crud.membership.organizer_membership import (
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
# 1. List members
# ------------------------------------------------------------
@router.get("/", response_model=List[OrganizerMembershipResponse])
def list_members(
    organizer_uuid: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_organizer_admin(user, organizer_uuid)
    return list_members_by_organizer(db, organizer_uuid)


# ------------------------------------------------------------
# 2. Add member
# ------------------------------------------------------------
@router.post("/", response_model=OrganizerMembershipResponse)
def add_member(
    organizer_uuid: str,
    data: OrganizerMembershipCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_organizer_admin(user, organizer_uuid)

    exist = get_membership(db, data.user_uuid, organizer_uuid)
    if exist and not exist.is_deleted:
        raise HTTPException(400, "User already a member")

    membership = create_membership(db, {
        "user_uuid": data.user_uuid,
        "organizer_uuid": organizer_uuid,
        "role": data.role,
        "created_by": user.user_uuid,
        "created_by_role": "organizer_admin",
    })

    return membership


# ------------------------------------------------------------
# 3. Update member
# ------------------------------------------------------------
@router.put("/{user_uuid}", response_model=OrganizerMembershipResponse)
def update_member(
    organizer_uuid: str,
    user_uuid: str,
    data: OrganizerMembershipUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_organizer_admin(user, organizer_uuid)

    membership = update_membership(db, user_uuid, organizer_uuid, data)
    if not membership:
        raise HTTPException(404, "Membership not found")

    return membership


# ------------------------------------------------------------
# 4. Delete member
# ------------------------------------------------------------
@router.delete("/{user_uuid}")
def delete_member(
    organizer_uuid: str,
    user_uuid: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_organizer_admin(user, organizer_uuid)

    deleted = soft_delete_membership(
        db,
        user_uuid,
        organizer_uuid,
        deleted_by=user.user_uuid,
        deleted_by_role="organizer_admin",
    )

    if not deleted:
        raise HTTPException(404, "Membership not found")

    return {"deleted": True}
