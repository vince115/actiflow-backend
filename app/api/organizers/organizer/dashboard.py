# app/api/organizers/organizer/dashboard.py
# Organizer 後台 - Dashboard（owner / admin）

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID

from app.core.db import get_db
from app.core.rbac import require_organizer_role

from app.schemas.organizer.dashboard import (
    OrganizerDashboardResponse,
    OrganizerDashboardStats,
)

from app.models.event.event import Event
from app.models.membership.organizer_membership import OrganizerMembership


router = APIRouter(
    prefix="/dashboard",
    tags=["Organizer - Dashboard"],
)


@router.get(
    "",
    response_model=OrganizerDashboardResponse,
    dependencies=[Depends(require_organizer_role(["owner", "admin"]))],
)
def get_dashboard(
    organizer_uuid: UUID,
    db: Session = Depends(get_db),
):
    """
    Organizer 後台 Dashboard（UX 用）
    """

    # members count
    members_count = (
        db.query(func.count(OrganizerMembership.user_uuid))
        .filter(
            OrganizerMembership.organizer_uuid == organizer_uuid,
            OrganizerMembership.is_deleted == False,
        )
        .scalar()
        or 0
    )

    # events count
    events_count = (
        db.query(func.count(Event.uuid))
        .filter(
            Event.organizer_uuid == organizer_uuid,
            Event.is_deleted == False,
        )
        .scalar()
        or 0
    )

    # UX 階段：先給 0，之後再補
    active_events = 0
    submissions_last_7_days = 0

    return OrganizerDashboardResponse(
        organizer_uuid=organizer_uuid,
        organizer_name="Organizer",  # 可之後補真資料
        stats=OrganizerDashboardStats(
            members_count=members_count,
            events_count=events_count,
            active_events=active_events,
            submissions_last_7_days=submissions_last_7_days,
        ),
    )
