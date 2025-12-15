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
    super_admin / organizer / user 都從這裡登入
    """

    # 1. 查詢使用者
    user = user_crud.get_by_email(db, data.email)

    # ⚠️ 不暴露「帳號是否存在」細節
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 2. 驗證密碼
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. 建立 Access Token
    access_token = create_access_token({
        "sub": str(user.uuid),
        "role": user.role
    })

    # 4. 建立 Refresh Token（寫入 DB）
    refresh_token_obj = refresh_token_crud.create_token(
        db=db,
        user_id=user.id,
        user_agent=request.headers.get("User-Agent", "unknown"),
    )

    # 5. 寫入 Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=60 * 15,  # 15 分鐘
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token_obj.token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,  # 30 天
    )

    # 6.  回傳登入成功（❌ 不回傳 token 本體）
    return {
        "success": True,
        "user": {
            "uuid": str(user.uuid),
            "email": user.email,
            "role": user.role,
        },
    }
