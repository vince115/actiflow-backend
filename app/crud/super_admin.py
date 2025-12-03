# app/crud/super_admin.py

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from passlib.context import CryptContext

from app.models.super_admin import SuperAdmin
from app.schemas.super_admin import SuperAdminCreate, SuperAdminUpdateRole
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------------------------------------------
# 密碼加密 / 驗證
# ------------------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ------------------------------------------------------------
# Create SuperAdmin
# ------------------------------------------------------------
def create_super_admin(db: Session, data: SuperAdminCreate) -> SuperAdmin:
    admin = SuperAdmin(
        email=data.email,
        name=data.name,
        phone=data.phone,
        password_hash=hash_password(data.password),
        is_active=True,
        is_deleted=False,
        created_by=data.created_by or "system",
        created_by_role=data.created_by_role or "system",
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


# ------------------------------------------------------------
# Read
# ------------------------------------------------------------
def get_super_admin_by_email(db: Session, email: str) -> SuperAdmin | None:
    return (
        db.query(SuperAdmin)
        .filter(
            SuperAdmin.email == email,
            SuperAdmin.is_deleted == False,
        )
        .first()
    )


def get_super_admin_by_uuid(db: Session, admin_uuid: str) -> SuperAdmin | None:
    try:
        admin_uuid = UUID(admin_uuid)
    except:
        return None

    return (
        db.query(SuperAdmin)
        .filter(
            SuperAdmin.uuid == admin_uuid,
            SuperAdmin.is_deleted == False,
        )
        .first()
    )


# ------------------------------------------------------------
# List all SuperAdmins
# ------------------------------------------------------------
def list_super_admins(db: Session):
    return (
        db.query(SuperAdmin)
        .filter(SuperAdmin.is_deleted == False)
        .order_by(SuperAdmin.created_at.asc())
        .all()
    )


# ------------------------------------------------------------
# Update SuperAdmin Role or Basic Info
# ------------------------------------------------------------
def update_super_admin_role(
    db: Session,
    admin_uuid: str,
    data: SuperAdminUpdateRole
):
    admin = get_super_admin_by_uuid(db, admin_uuid)
    
    # 防止 NoneType crash
    if not admin:
        return None

    # 狀態檢查
    if admin.is_deleted:
        return None
    if not admin.is_active:
        return None

    # 動態更新欄位
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(admin, field, value)

    admin.updated_at = datetime.now(timezone.utc)
    admin.updated_by = data.updated_by
    admin.updated_by_role = data.updated_by_role

    db.commit()
    db.refresh(admin)
    return admin


# ------------------------------------------------------------
# Soft Delete SuperAdmin
# ------------------------------------------------------------
def delete_super_admin(
    db: Session,
    admin_uuid: str,
    deleted_by: str,
    deleted_by_role: str = "super_admin"
):
    admin = get_super_admin_by_uuid(db, admin_uuid)
    if not admin:
        return None

    admin.is_deleted = True
    admin.deleted_at = datetime.now(timezone.utc)
    admin.deleted_by = deleted_by
    admin.deleted_by_role = deleted_by_role

    db.commit()
    return admin
