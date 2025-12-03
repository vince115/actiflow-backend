# app/crud/organizer_application.py

from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.organizer_application import OrganizerApplication


def get_application(db: Session, application_uuid: str):
    return db.query(OrganizerApplication).filter(
        OrganizerApplication.uuid == application_uuid,
        OrganizerApplication.is_deleted == False
    ).first()


def list_applications(db: Session, status: str | None = None):
    query = db.query(OrganizerApplication).filter(
        OrganizerApplication.is_deleted == False
    )
    if status:
        query = query.filter(OrganizerApplication.status == status)

    return query.order_by(OrganizerApplication.submitted_at.desc()).all()


def review_application(db: Session, app: OrganizerApplication, new_status: str, reviewer_uuid: str, reviewer_role: str, reason: str | None = None):
    app.status = new_status
    app.reviewed_at = datetime.now(timezone.utc)
    app.reviewer_uuid = reviewer_uuid
    app.reviewer_role = reviewer_role
    app.reason = reason

    db.commit()
    db.refresh(app)
    return app
