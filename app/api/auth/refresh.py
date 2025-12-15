# app/api/auth/refresh.py

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.db import get_db
from app.core.jwt import create_access_token
from app.models.user.user import User
from app.crud.user.crud_refresh_token import refresh_token_crud

router = APIRouter(tags=["Auth"])


@router.post("/refresh")
def refresh_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    使用 refresh_token 換取新的 access_token。
    """

    # 1. 從 cookie 取得 refresh_token
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    # 2. 查詢 DB refresh token
    db_token = refresh_token_crud.get_by_token(db, refresh_token)

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # 3. 查詢 user
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 4. 建立新的 Access Token
    new_access_token = create_access_token({
        "sub": str(user.uuid),
        "role": user.role
    })

    # 5. 寫回 Cookie（覆蓋舊的 access_token）
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        samesite="lax",
        secure=False,   # 本地測試用，部署 Cloud Run 改成 True
        max_age=60 * 15,  # 15 分鐘
    )

    return {
        "success": True,
        "access_token": new_access_token,
        "user": {
            "uuid": str(user.uuid),
            "email": user.email,
            "role": user.role
        }
    }
