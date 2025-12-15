# app/crud/membership/crud_organizer_membership.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.membership.organizer_membership import OrganizerMembership
from app.schemas.membership.organizer.organizer_membership_create import (
    OrganizerMembershipCreate,
)
from app.schemas.membership.organizer.organizer_membership_update import (
    OrganizerMembershipUpdate,
)


# ============================================================
# Query helpers
# ============================================================

def get_membership_by_user_and_organizer(
    db: Session,
    user_uuid: str,
    organizer_uuid: str,
) -> OrganizerMembership | None:
    return (
        db.query(OrganizerMembership)
        .filter(
            OrganizerMembership.user_uuid == user_uuid,
            OrganizerMembership.organizer_uuid == organizer_uuid,
            OrganizerMembership.is_deleted == False,
        )
        .first()
    )


def get_membership_by_uuid(
    db: Session,
    membership_uuid: str,
) -> OrganizerMembership | None:
    return (
        db.query(OrganizerMembership)
        .filter(
            OrganizerMembership.uuid == membership_uuid,
            OrganizerMembership.is_deleted == False,
        )
        .first()
    )


def list_members_by_organizer(
    db: Session,
    organizer_uuid: str,
) -> list[OrganizerMembership]:
    return (
        db.query(OrganizerMembership)
        .filter(
            OrganizerMembership.organizer_uuid == organizer_uuid,
            OrganizerMembership.is_deleted == False,
        )
        .order_by(OrganizerMembership.created_at.asc())
        .all()
    )


def list_user_memberships(
    db: Session,
    user_uuid: str,
) -> list[OrganizerMembership]:
    return (
        db.query(OrganizerMembership)
        .filter(
            OrganizerMembership.user_uuid == user_uuid,
            OrganizerMembership.is_deleted == False,
        )
        .order_by(OrganizerMembership.created_at.asc())
        .all()
    )


# ============================================================
# Create
# ============================================================

def create_membership(
    db: Session,
    data: OrganizerMembershipCreate,
    created_by: str,
    created_by_role: str,
) -> OrganizerMembership:
    membership = OrganizerMembership(
        **data.model_dump(),
        created_by=created_by,
        created_by_role=created_by_role,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


# ============================================================
# Update
# ============================================================

def update_membership(
    db: Session,
    membership: OrganizerMembership,
    data: OrganizerMembershipUpdate,
    updated_by: str,
    updated_by_role: str,
) -> OrganizerMembership:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(membership, field, value)

    membership.updated_by = updated_by
    membership.updated_by_role = updated_by_role

    db.commit()
    db.refresh(membership)
    return membership


# ============================================================
# Soft delete
# ============================================================

def soft_delete_membership(
    db: Session,
    membership: OrganizerMembership,
    deleted_by: str,
    deleted_by_role: str,
) -> OrganizerMembership:
    membership.is_deleted = True
    membership.deleted_by = deleted_by
    membership.deleted_by_role = deleted_by_role

    db.commit()
    db.refresh(membership)
    return membership


# ============================================================
# Organizer owner transfer
# ============================================================

def set_organizer_owner(
    db: Session,
    organizer_uuid: str,
    new_owner_user_uuid: str,
    updated_by: str,
    updated_by_role: str,
) -> bool:
    """
    將 organizer 的 owner 轉移給指定 user
    - 同一 organizer 永遠只會有一個 owner
    - 舊 owner 降級為 admin
    """

    try:
        # 1. 目前 owner
        current_owner = (
            db.query(OrganizerMembership)
            .filter(
                OrganizerMembership.organizer_uuid == organizer_uuid,
                OrganizerMembership.role == "owner",
                OrganizerMembership.is_deleted == False,
            )
            .one_or_none()
        )

        # 2. 目標 membership
        target = (
            db.query(OrganizerMembership)
            .filter(
                OrganizerMembership.organizer_uuid == organizer_uuid,
                OrganizerMembership.user_uuid == new_owner_user_uuid,
                OrganizerMembership.is_deleted == False,
            )
            .one_or_none()
        )

        if not target:
            return False

        # 3. 如果已經是 owner，直接成功
        if current_owner and current_owner.uuid == target.uuid:
            return True

        # 4. 降級舊 owner
        if current_owner:
            current_owner.role = "admin"
            current_owner.updated_by = updated_by
            current_owner.updated_by_role = updated_by_role

        # 5. 升級新 owner
        target.role = "owner"
        target.updated_by = updated_by
        target.updated_by_role = updated_by_role

        db.commit()
        return True

    except SQLAlchemyError:
        db.rollback()
        return False
