# app/crud/organizer/crud_organizer_application.py

from sqlalchemy.orm import Session
from app.models.organizer.organizer_application import OrganizerApplication


# -----------------------------
# 建立申請（User 送出）
# -----------------------------
def create_application(
    db: Session,
    user_uuid: str,
    organizer_uuid: str,
    name: str,
    email: str,
    message: str
):
    application = OrganizerApplication(
        user_uuid=user_uuid,
        organizer_uuid=organizer_uuid,
        applicant_name=name,
        applicant_email=email,
        message=message,
        status="pending",
    )

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


# -----------------------------
# 使用者查詢自己的申請
# -----------------------------
def list_user_applications(db: Session, user_uuid: str):
    return (
        db.query(OrganizerApplication)
        .filter(OrganizerApplication.user_uuid == user_uuid)
        .order_by(OrganizerApplication.created_at.desc())
        .all()
    )


# -----------------------------
# Organizer 管理者查詢本單位申請
# -----------------------------
def list_organizer_applications(db: Session, organizer_uuid: str):
    return (
        db.query(OrganizerApplication)
        .filter(OrganizerApplication.organizer_uuid == organizer_uuid)
        .order_by(OrganizerApplication.created_at.desc())
        .all()
    )


# -----------------------------
# Admin 查看全平台申請
# -----------------------------
def list_all_applications(db: Session):
    return (
        db.query(OrganizerApplication)
        .order_by(OrganizerApplication.created_at.desc())
        .all()
    )


# -----------------------------
# 單一申請
# -----------------------------
def get_application(db: Session, app_id: int):
    return db.query(OrganizerApplication).filter(OrganizerApplication.id == app_id).first()


# -----------------------------
# 審核（通過 / 拒絕）
# -----------------------------
def review_application(
    db: Session,
    application: OrganizerApplication,
    status: str,
    reviewer_uuid: str = None
):
    application.status = status
    application.reviewed_by = reviewer_uuid

    db.commit()
    db.refresh(application)
    return application
