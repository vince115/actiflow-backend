# app/crud/organizer.py

from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.organizer import Organizer
from app.schemas.organizer import OrganizerCreate, OrganizerUpdate


# ------------------------------------------------------------
# 建立 Organizer（僅限 system_admin 使用）
# ------------------------------------------------------------
def create_organizer(db: Session, data: OrganizerCreate) -> Organizer:

    organizer = Organizer(
        organizer_uuid=data.organizer_uuid,   # 外部企業代碼
        name=data.name,
        email=data.email,
        phone=data.phone,
        address=data.address,
        website=data.website,
        description=data.description,
        created_by=data.created_by,
        created_by_role=data.created_by_role,
    )

    db.add(organizer)
    db.commit()
    db.refresh(organizer)
    return organizer


# ------------------------------------------------------------
# 依 uuid 查詢（主鍵）
# ------------------------------------------------------------
def get_organizer_by_uuid(db: Session, uuid: str) -> Optional[Organizer]:
    return db.query(Organizer).filter(
        Organizer.uuid == uuid,
        Organizer.is_deleted == False
    ).first()


# ------------------------------------------------------------
# 依 organizer_uuid（外部代碼）查詢
# ------------------------------------------------------------
def get_organizer_by_id(db: Session, organizer_uuid: str) -> Optional[Organizer]:
    return db.query(Organizer).filter(
        Organizer.organizer_uuid == organizer_uuid,
        Organizer.is_deleted == False
    ).first()


# ------------------------------------------------------------
# 依 Email 查詢（用於平台搜尋）
# ------------------------------------------------------------
def get_organizer_by_email(db: Session, email: str) -> Optional[Organizer]:
    return db.query(Organizer).filter(
        Organizer.email == email,
        Organizer.is_deleted == False
    ).first()


# ------------------------------------------------------------
# 取得全部 Organizer（僅 system_admin 可用）
# ------------------------------------------------------------
def list_organizers(db: Session) -> List[Organizer]:
    return db.query(Organizer).filter(
        Organizer.is_deleted == False
    ).all()


# ------------------------------------------------------------
# 更新 Organizer（公司資料）
# ------------------------------------------------------------
def update_organizer(
    db: Session,
    uuid: str,
    data: OrganizerUpdate
) -> Optional[Organizer]:

    organizer = get_organizer_by_uuid(db, uuid)
    if not organizer:
        return None
    
    # 更新欄位
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(organizer, field, value)

    db.commit()
    db.refresh(organizer)
    return organizer


# ------------------------------------------------------------
# 軟刪除 Organizer
# ------------------------------------------------------------
def soft_delete_organizer(db: Session, uuid: str) -> Optional[Organizer]:
    organizer = get_organizer_by_uuid(db, uuid)
    if not organizer:
        return None

    organizer.is_deleted = True
    db.commit()
    return organizer
