# app/core/db.py ← 資料庫 Session, engine, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings


# ---------------------------------------------------------
# Database URL (sync)
# ---------------------------------------------------------
DATABASE_URL = settings.db_url

print("DATABASE_URL =", DATABASE_URL)  # ← 正確印出當前連線的資料庫 URL

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is missing! Check your .env file.")

# ---------------------------------------------------------
# Sync Engine（FastAPI CRUD 與 Alembic 使用）
# ---------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)

Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
