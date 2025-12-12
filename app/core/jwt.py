# app/core/jwt.py  ← JWT 產生、驗證

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status
from app.core.config import settings
import uuid

ALGORITHM = settings.ALGORITHM


def create_access_token(data: dict, expires_minutes: int = 60):
    """
    建立 JWT Access Token（支援 exp / iat / jti）
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    issued_at = datetime.now(timezone.utc)

    to_encode.update({
        "exp": expire,
        "iat": issued_at,
        "jti": str(uuid.uuid4())  # 用於 future token blacklist/revoke
    })

    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """
    解碼與驗證 Access Token
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM]
        )
        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        )


def create_login_token(user_uuid: str, role: str):
    """
    通用登入 Token 產生器
    - 統一角色名稱（super_admin / organizer_admin / user ...）
    """
    return create_access_token({
        "sub": user_uuid,
        "role": role,
    })
