# app/api/organizers/organizer/members.py
# Organizer 後台 - 成員管理（owner / admin）

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_organizer_admin

from app.crud.membership.crud_organizer_membership import (
    list_members_by_organizer,
    get_membership_by_user_and_organizer,
    create_membership,
    update_membership,
    soft_delete_membership,
    set_organizer_owner,
)

from app.schemas.membership.organizer.organizer_membership_create import (
    OrganizerMembershipCreate,
)
from app.schemas.membership.organizer.organizer_membership_update import (
    OrganizerMembershipUpdate,
)
from app.schemas.membership.organizer.organizer_membership_response import (
    OrganizerMembershipResponse,
)

router = APIRouter(
    prefix="/organizer/members",
    tags=["Organizer - Members"],
)


# -------------------------------------------------------------------
# List organizer members
# -------------------------------------------------------------------
@router.get("", response_model=list[OrganizerMembershipResponse])
def list_members(
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer 後台：
    列出該 organizer 的所有成員
    """
    members = list_members_by_organizer(
        db=db,
        organizer_uuid=membership.organizer_uuid,
    )

    return [
        OrganizerMembershipResponse.model_validate(m)
        for m in members
    ]


# -------------------------------------------------------------------
# Add member
# -------------------------------------------------------------------
@router.post("", response_model=OrganizerMembershipResponse)
def add_member(
    data: OrganizerMembershipCreate,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer 後台：
    新增成員（owner / admin）
    """

    # 不允許重複加入
    exist = get_membership_by_user_and_organizer(
        db=db,
        user_uuid=data.user_uuid,
        organizer_uuid=membership.organizer_uuid,
    )

    if exist and not exist.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="User already a member of this organizer",
        )

    new_member = create_membership(
        db=db,
        user_uuid=data.user_uuid,
        organizer_uuid=membership.organizer_uuid,
        role=data.role,
        created_by=membership.user_uuid,
        created_by_role=membership.role,
    )

    return OrganizerMembershipResponse.model_validate(new_member)


# -------------------------------------------------------------------
# Update member role
# -------------------------------------------------------------------
@router.put("/{user_uuid}", response_model=OrganizerMembershipResponse)
def update_member(
    user_uuid: UUID,
    data: OrganizerMembershipUpdate,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer 後台：
    更新成員角色
    """

    target = get_membership_by_user_and_organizer(
        db=db,
        user_uuid=user_uuid,
        organizer_uuid=membership.organizer_uuid,
    )

    if not target or target.is_deleted:
        raise HTTPException(status_code=404, detail="Membership not found")

    updated = update_membership(
        db=db,
        membership=target,
        data=data,
        updated_by=membership.user_uuid,
        updated_by_role=membership.role,
    )

    return OrganizerMembershipResponse.model_validate(updated)


# -------------------------------------------------------------------
# Remove member (soft delete)
# -------------------------------------------------------------------
@router.delete("/{user_uuid}")
def delete_member(
    user_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer 後台：
    移除成員（軟刪除）
    """

    target = get_membership_by_user_and_organizer(
        db=db,
        user_uuid=user_uuid,
        organizer_uuid=membership.organizer_uuid,
    )

    if not target or target.is_deleted:
        raise HTTPException(status_code=404, detail="Membership not found")

    # 不允許刪除自己（避免自殺）
    if target.user_uuid == membership.user_uuid:
        raise HTTPException(
            status_code=400,
            detail="You cannot remove yourself",
        )

    soft_delete_membership(
        db=db,
        membership=target,
        deleted_by=membership.user_uuid,
        deleted_by_role=membership.role,
    )

    return {"deleted": True, "user_uuid": user_uuid}


# -------------------------------------------------------------------
# Transfer organizer ownership
# -------------------------------------------------------------------
@router.post("/{user_uuid}/transfer-ownership")
def transfer_ownership(
    user_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer 後台：
    將 owner 轉移給指定成員
    ※ 只有現任 owner 可以操作
    """

    if membership.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owner can transfer ownership",
        )

    target = get_membership_by_user_and_organizer(
        db=db,
        user_uuid=user_uuid,
        organizer_uuid=membership.organizer_uuid,
    )

    if not target or target.is_deleted:
        raise HTTPException(status_code=404, detail="Target member not found")

    success = set_organizer_owner(
        db=db,
        organizer_uuid=membership.organizer_uuid,
        new_owner_user_uuid=user_uuid,
        updated_by=membership.user_uuid,
        updated_by_role=membership.role,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to transfer ownership",
        )

    return {
        "message": "Ownership transferred",
        "organizer_uuid": membership.organizer_uuid,
        "new_owner_user_uuid": user_uuid,
    }
