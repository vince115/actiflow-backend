# tests/conftest.py

import os
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.db import SessionLocal


@pytest.fixture(scope="session", autouse=True)
def _force_test_env():
    # 確保走 settings.db_url -> TEST_DATABASE_URL
    os.environ.setdefault("ENV", "test")


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
        session.rollback()
    finally:
        session.close()


@pytest.fixture
def client():
    # TestClient 會保留 cookie，適合測 session/cookie auth
    return TestClient(app)

