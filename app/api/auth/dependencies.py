# app/api/auth/dependencies.py

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.jwt import decode_access_token
from app.models.user.user import User
from app.api.auth.identity import build_identity

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> dict:
    """
    Unified auth dependency.
    Returns a dict compatible with /auth/me response.
    """

    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    payload = decode_access_token(access_token)
    user_uuid = payload.get("sub")
    if not user_uuid:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user = (
        db.query(User)
        .filter(User.uuid == user_uuid, User.is_deleted == False)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return build_identity(db, user)