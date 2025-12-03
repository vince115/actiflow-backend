# app/api/auth/super_admin_auth.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.jwt import create_login_token
from app.core.db import get_db

from app.crud.super_admin import (
    get_super_admin_by_email,
    verify_password
)

router = APIRouter(prefix="/super-admin", tags=["SuperAdmin Auth"])


@router.post("/login")
def super_admin_login(
    email: str, 
    password: str,
    db: Session = Depends(get_db)
):
    """
    超級管理者是寫死在 .env 的
    SUPER_ADMIN_EMAIL
    SUPER_ADMIN_PASSWORD
    """
    admin = get_super_admin_by_email(db, email)
    if not admin:
        raise HTTPException(400, "Super admin not found")
    
    # 驗證密碼
    if not verify_password(password, admin.password_hash):
        raise HTTPException(400, "Incorrect password")

    # 使用 admin.uuid 與 role="super_admin"
    token = create_login_token(
        user_uuid=str(admin.uuid),
        role="super_admin"
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "uuid": str(admin.uuid),
        "role": "super_admin",
        "name": admin.name,
        "email": admin.email,
    }