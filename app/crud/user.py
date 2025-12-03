# app/crud/user.py

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timezone

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------------------------------------------
# 密碼功能
# ------------------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ------------------------------------------------------------
# Create User
# ------------------------------------------------------------
def create_user(db: Session, data: UserCreate):

    user = User(
        email=data.email,
        name=data.name,
        phone=data.phone,
        avatar_url=data.avatar_url,

        # password（email 註冊才需要）
        password_hash=hash_password(data.password) if data.password else None,

        # 第三方登入 provider
        auth_provider=data.auth_provider or "local",

        # 其他補充資料
        config=data.config or {},
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ------------------------------------------------------------
# Read
# ------------------------------------------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.email == email,
        User.is_deleted == False
    ).first()


def get_user_by_uuid(db: Session, uuid: str):
    return db.query(User).filter(
        User.uuid == uuid,
        User.is_deleted == False
    ).first()


# ------------------------------------------------------------
# Update
# ------------------------------------------------------------
def update_user(db: Session, uuid: str, data: UserUpdate):

    user = get_user_by_uuid(db, uuid)
    if not user:
        return None

    # 動態更新資料
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    # 🔥 補上 updated_at
    user.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)
    return user


# ------------------------------------------------------------
# Soft Delete
# ------------------------------------------------------------
def soft_delete_user(db: Session, uuid: str):
    user = get_user_by_uuid(db, uuid)
    if not user:
        return None

    user.is_deleted = True
    db.commit()
    return user


# ------------------------------------------------------------
# List Users (New)
# ------------------------------------------------------------
def list_users(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    """
    回傳尚未被軟刪除的使用者清單。
    skip / limit 支援簡易分頁。
    """
    return (
        db.query(User)
        .filter(User.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )

# ------------------------------------------------------------
# SuperAdmin: 強制重置密碼
# ------------------------------------------------------------
def force_reset_password(db: Session, uuid: str, new_password: str = "Temp@1234"):
    user = get_user_by_uuid(db, uuid)
    if not user:
        return None

    user.password_hash = hash_password(new_password)
    user.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)
    return new_password


# ------------------------------------------------------------
# SuperAdmin: 強制停用使用者
# ------------------------------------------------------------
def disable_user_account(db: Session, uuid: str):
    user = get_user_by_uuid(db, uuid)
    if not user:
        return None

    user.is_active = False
    user.updated_at = datetime.now(timezone.utc)

    db.commit()
    return True
