# app/api/organizers/organizer/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.db import get_db
from app.api.organizers.dependencies import require_organizer_admin

from app.schemas.organizer.dashboard import DashboardResponse
from app.schemas.event.core.event_response import EventResponse
from app.schemas.organizer_application.organizer_application_response import (
    OrganizerApplicationResponse,
)

from app.models.event.event import Event
from app.models.organizer.organizer_application import OrganizerApplication
from app.models.membership.organizer_membership import OrganizerMembership

router = APIRouter(
    prefix="/organizers/dashboard",
    tags=["Organizer Dashboard"],
)


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin),
):
    organizer_uuid = membership.organizer_uuid

    # 1. Counts
    events_count = (
        db.query(func.count(Event.uuid))
        .filter(
            Event.organizer_uuid == organizer_uuid,
            Event.is_deleted == False,
        )
        .scalar()
    )

    members_count = (
        db.query(func.count(OrganizerMembership.user_uuid))
        .filter(
            OrganizerMembership.organizer_uuid == organizer_uuid,
            OrganizerMembership.is_deleted == False,
        )
        .scalar()
    )

    pending_applications_count = (
        db.query(func.count(OrganizerApplication.uuid))
        .filter(
            OrganizerApplication.organizer_uuid == organizer_uuid,
            OrganizerApplication.status == "pending",
            OrganizerApplication.is_deleted == False,
        )
        .scalar()
    )

    # 2. Recent Events (limit 5)
    recent_events_objs = (
        db.query(Event)
        .filter(
            Event.organizer_uuid == organizer_uuid,
            Event.is_deleted == False,
        )
        .order_by(Event.created_at.desc())
        .limit(5)
        .all()
    )
    recent_events = [EventResponse.model_validate(e) for e in recent_events_objs]

    # 3. Recent Applications (limit 5)
    recent_applications_objs = (
        db.query(OrganizerApplication)
        .filter(
            OrganizerApplication.organizer_uuid == organizer_uuid,
            OrganizerApplication.is_deleted == False,
        )
        .order_by(OrganizerApplication.created_at.desc())
        .limit(5)
        .all()
    )
    recent_applications = [
        OrganizerApplicationResponse.model_validate(a)
        for a in recent_applications_objs
    ]

    return DashboardResponse(
        events_count=events_count or 0,
        members_count=members_count or 0,
        pending_applications_count=pending_applications_count or 0,
        recent_events=recent_events,
        recent_applications=recent_applications,
    )
