# app/api/auth/login.py

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.db import get_db
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.config import settings

from app.crud.user.crud_user import user_crud
from app.crud.user.crud_refresh_token import refresh_token_crud

router = APIRouter(tags=["Auth"])


# ------------------------------------------------------------
# Login input schema
# ------------------------------------------------------------
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

# ------------------------------------------------------------
# Unified Login API
# ------------------------------------------------------------
@router.post("/login")
def unified_login(
    data: LoginSchema,
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    統一登入 API
    - 只負責身份驗證
    - 不處理角色、不處理平台
    """

    # 1. 查詢使用者
    user = user_crud.get_by_email(db, data.email)

    # ⚠️ 不暴露帳號是否存在
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 2. 驗證密碼
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. 建立 Access Token（只放 identity）
    access_token = create_access_token({
        "sub": str(user.uuid),
        "type": "user",   # optional：未來擴充用
    })

    # 4. 建立 Refresh Token
    refresh_token_obj = refresh_token_crud.create_token(
        db=db,
        user_uuid=user.uuid,
        user_agent=request.headers.get("User-Agent", "unknown"),
    )

    # 5. 寫入 Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=60 * 15,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token_obj.token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    # 6. 回傳登入成功（不含 token）
    return {
        "success": True,
        "user": {
            "uuid": str(user.uuid),
            "email": user.email,
        },
    }

