# app/core/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ---------------------------------------------------------
# Database URL (sync)
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# ---------------------------------------------------------
# Sync Engine（FastAPI CRUD 與 Alembic 使用）
# ---------------------------------------------------------
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# ---------------------------------------------------------
# Base for Models
# ---------------------------------------------------------
Base = declarative_base()

# ---------------------------------------------------------
# FastAPI dependency - 標準命名 get_db()
# ---------------------------------------------------------
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
