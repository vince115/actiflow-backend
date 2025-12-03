# app/crud/settings.py
from sqlalchemy.orm import Session
from app.models.settings import SystemSettings
from app.schemas.settings import SystemSettingsUpdate


def get_system_settings(db: Session) -> SystemSettings:
    """取得系統唯一設定（沒有就建立）"""
    settings = db.query(SystemSettings).first()

    if not settings:
        settings = SystemSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


def update_system_settings(db: Session, data: SystemSettingsUpdate) -> SystemSettings:
    settings = get_system_settings(db)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(settings, field, value)

    db.commit()
    db.refresh(settings)
    return settings
