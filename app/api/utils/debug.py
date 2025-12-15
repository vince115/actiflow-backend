# app/api/utils/debug.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.config import settings

from app.crud.user.crud_user import user_crud

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.post("/reset-admin-password")
def reset_admin_password(db: Session = Depends(get_db)):
    """
    ⚠️ DEV ONLY
    重置 admin@example.com 的密碼
    """
    if settings.ENV != "dev":
        # 在 staging / prod 直接當不存在
        raise HTTPException(status_code=404, detail="Not found")

    user = user_crud.get_by_email(db, "admin@example.com")
    if not user:
        return {"detail": "Admin user not found"}

    new_pw = user_crud.force_reset_password(db, user.uuid)

    return {
        "reset": True,
        "email": user.email,
        "new_password": new_pw,
    }