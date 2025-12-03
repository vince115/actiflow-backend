# app/crud/organizer_membership.py

from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.organizer_membership import OrganizerMembership
from app.schemas.organizer_membership import (
    OrganizerMembershipCreate,
    OrganizerMembershipUpdate
)


# ------------------------------------------------------------
# 建立 Membership（使用者加入主辦單位）
# ------------------------------------------------------------
def create_membership(db: Session, data: OrganizerMembershipCreate):
    """
    建立 user ↔ organizer 的 membership
    role 預設為 member
    """

    membership = OrganizerMembership(
        user_uuid=data.user_uuid,
        organizer_uuid=data.organizer_uuid,
        role=data.role or "member",
        status=data.status or "active",
        created_by=data.created_by,
        created_by_role=data.created_by_role
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


# ------------------------------------------------------------
#     取得某個 Organizer 底下的所有會員（含 owner / admin / member）
# ------------------------------------------------------------
def list_members_by_organizer(db: Session, organizer_uuid: str):
    """
    - 排除 is_deleted = True
    - 顯示 active 的 membership
    """
    return (
        db.query(OrganizerMembership)
        .filter(
            OrganizerMembership.organizer_uuid == organizer_uuid,
            OrganizerMembership.is_deleted == False
        )
        .order_by(OrganizerMembership.created_at.asc())
        .all()
    )

# ------------------------------------------------------------
# 查詢某 user 與某 organizer 的 membership
# ------------------------------------------------------------
def get_membership(db: Session, user_uuid: str, organizer_uuid: str):
    return db.query(OrganizerMembership).filter(
        OrganizerMembership.user_uuid == user_uuid,
        OrganizerMembership.organizer_uuid == organizer_uuid,
        OrganizerMembership.is_deleted == False
    ).first()


# ------------------------------------------------------------
# 更新 Membership（role, status, is_active）
# ------------------------------------------------------------
def update_membership(
    db: Session,
    user_uuid: str,
    organizer_uuid: str,
    data: OrganizerMembershipUpdate
):
    membership = get_membership(db, user_uuid, organizer_uuid)
    if not membership:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(membership, field, value)

    db.commit()
    db.refresh(membership)
    return membership


# ------------------------------------------------------------
# 取得某使用者加入的所有主辦單位
# ------------------------------------------------------------
def get_user_memberships(db: Session, user_uuid: str) -> List[OrganizerMembership]:
    return db.query(OrganizerMembership).filter(
        OrganizerMembership.user_uuid == user_uuid,
        OrganizerMembership.is_deleted == False
    ).all()


# ------------------------------------------------------------
# 取得主辦單位的所有成員
# ------------------------------------------------------------
def get_organizer_members(db: Session, organizer_uuid: str) -> List[OrganizerMembership]:
    return db.query(OrganizerMembership).filter(
        OrganizerMembership.organizer_uuid == organizer_uuid,
        OrganizerMembership.is_deleted == False
    ).all()


# ------------------------------------------------------------
# 軟刪除 Membership（退出主辦單位）
# ------------------------------------------------------------
def soft_delete_membership(db: Session, user_uuid: str, organizer_uuid: str):
    membership = get_membership(db, user_uuid, organizer_uuid)
    if not membership:
        return None

    membership.is_deleted = True
    db.commit()
    return membership


# ------------------------------------------------------------
# 檢查主辦單位是否至少有一位 owner
# ------------------------------------------------------------
def ensure_owner_exists(db: Session, organizer_uuid: str) -> bool:
    owner = db.query(OrganizerMembership).filter(
        OrganizerMembership.organizer_uuid == organizer_uuid,
        OrganizerMembership.role == "owner",
        OrganizerMembership.is_deleted == False
    ).first()

    return owner is not None
