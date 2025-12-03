# app/core/security.py

from passlib.context import CryptContext

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
