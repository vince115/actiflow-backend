# app/core/dependencies.py ← FastAPI DI 注入元件

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.jwt import decode_access_token
from app.models.user.user import User


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    從 Cookie 的 access_token 取得目前登入使用者。
    """

    # 1. 從 Cookie 取得 access_token
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Access token missing")

    # 2. Decode JWT
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    user_uuid = payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # 3. 查 DB 找 user
    user = db.query(User).filter(User.uuid == user_uuid).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.is_deleted or not user.is_active:
        raise HTTPException(status_code=401, detail="User inactive or deleted")

    return user
