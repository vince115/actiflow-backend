# app/crud/system_membership.py

from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone

from app.models.system_membership import SystemMembership
from app.schemas.system_membership import (
    SystemMembershipCreate,
    SystemMembershipUpdate
)


# ------------------------------------------------------------
# Create (assign platform role to user)
# ------------------------------------------------------------
def create_system_membership(db: Session, data: SystemMembershipCreate):
    membership = SystemMembership(
        user_uuid=data.user_uuid,
        role=data.role,
        status=data.status or "active",

        created_by=data.created_by,
        created_by_role=data.created_by_role,
        is_active=True,
        is_deleted=False
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


# ------------------------------------------------------------
# Get membership (by user)
# ------------------------------------------------------------
def get_system_membership(db: Session, user_uuid: str) -> Optional[SystemMembership]:
    return db.query(SystemMembership).filter(
        SystemMembership.user_uuid == user_uuid,
        SystemMembership.is_deleted == False
    ).first()



# ------------------------------------------------------------
# List all system memberships
# ------------------------------------------------------------
def list_system_memberships(db: Session) -> List[SystemMembership]:
    return db.query(SystemMembership).filter(
        SystemMembership.is_deleted == False
    ).all()


# ------------------------------------------------------------
# Update membership
# ------------------------------------------------------------
def update_system_membership(db: Session, user_uuid: str, data: SystemMembershipUpdate):
    membership = get_system_membership(db, user_uuid)
    if not membership:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(membership, field, value)

    membership.updated_by = data.updated_by
    membership.updated_by_role = data.updated_by_role
    membership.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(membership)
    return membership

# ------------------------------------------------------------
# Soft delete (remove platform role)
# ------------------------------------------------------------
def soft_delete_system_membership(
    db: Session,
    user_uuid: str,
    deleted_by: Optional[str] = None,
    deleted_by_role: Optional[str] = None
):
    membership = get_system_membership(db, user_uuid)
    if not membership:
        return None

    membership.is_deleted = True
    membership.deleted_at = datetime.now(timezone.utc)
    membership.deleted_by = deleted_by
    membership.deleted_by_role = deleted_by_role

    db.commit()
    return membership

# ------------------------------------------------------------
# Helper: get user platform role (system_admin / support / auditor)
# ------------------------------------------------------------
def get_user_platform_role(db: Session, user_uuid: str) -> Optional[str]:
    membership = get_system_membership(db, user_uuid)
    return membership.role if membership else None


# ------------------------------------------------------------
# Check if user is system_admin
# ------------------------------------------------------------
def is_system_admin(db: Session, user_uuid: str) -> bool:
    membership = get_system_membership(db, user_uuid)
    return (
        membership is not None and
        membership.role == "system_admin" and
        membership.is_active and
        not membership.is_deleted
    )