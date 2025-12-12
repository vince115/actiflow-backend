# app/core/security.py ← 密碼 Hash / JWT

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os

# ----------------------
# 密碼 Hash / Verify
# ----------------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """將明碼密碼 Hash 成 bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證明碼與 Hash 是否相符"""
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------
# JWT 設定
# ----------------------
# 若你想用環境變數，可改成 os.getenv("JWT_SECRET")
SECRET_KEY = os.getenv("JWT_SECRET", "CHANGE_THIS_SECRET_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ----------------------
# JWT：建立 Token
# ----------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    產生 Access Token
    data 會放入 payload，例如：{"sub": user.uuid, "role": user.role}
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ----------------------
# JWT：解析 Token
# ----------------------
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
