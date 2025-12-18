# app/api/auth/identity.py

from sqlalchemy.orm import Session

from app.models.user.user import User
from app.models.membership.system_membership import SystemMembership
from app.models.membership.organizer_membership import OrganizerMembership
from app.models.organizer.organizer import Organizer


def build_identity(db: Session, user: User) -> dict:
    """
    Build identity payload for RBAC and /auth/me
    """

    # ----------------------------
    # System memberships
    # ----------------------------
    system_memberships = (
        db.query(SystemMembership)
        .filter(
            SystemMembership.user_uuid == user.uuid,
            SystemMembership.is_deleted == False,
            SystemMembership.is_active == True,
            SystemMembership.is_suspended == False,
        )
        .all()
    )

    system_payload = [
        {
            "type": "system",
            "role": m.role,
            "status": "active",
        }
        for m in system_memberships
    ]

    # ----------------------------
    # Organizer memberships
    # ----------------------------
    organizer_memberships = (
        db.query(OrganizerMembership)
        .join(Organizer, Organizer.uuid == OrganizerMembership.organizer_uuid)
        .filter(
            OrganizerMembership.user_uuid == user.uuid,
            OrganizerMembership.is_deleted == False,
            OrganizerMembership.is_active == True,
            Organizer.is_deleted == False,
        )
        .all()
    )

    organizer_payload = [
        {
            "type": "organizer",
            "organizer_uuid": str(m.organizer_uuid),
            "organizer_name": m.organizer.name,
            "membership_role": m.role,
        }
        for m in organizer_memberships
    ]

    return {
        "uuid": str(user.uuid),
        "email": user.email,
        "memberships": [
            *system_payload,
            *organizer_payload,
        ],
    }
