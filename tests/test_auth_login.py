# tests/test_auth_login.py

from uuid import uuid4
from sqlalchemy.orm import Session

from app.models.user.user import User
from app.core.security import hash_password


def test_auth_login_sets_cookie_and_me_works(client, db: Session):
    email = f"login+{uuid4().hex}@test.com"
    password = "test1234"

    # 1) 建 user（直接寫進 Neon test branch）
    user = User(
        uuid=uuid4(),
        email=email,
        password_hash=hash_password(password),
        is_active=True,
    )
    db.add(user)
    db.commit()

    # 2) login -> 應該 set-cookie
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code in (200, 201)

    set_cookie = r.headers.get("set-cookie") or ""
    assert "access_token=" in set_cookie  # 你現在的核心行為

    # 3) 同一個 client 打 /auth/me -> 應該成功（cookie 已自動帶上）
    me = client.get("/auth/me")
    assert me.status_code == 200
    data = me.json()
    assert data["email"] == email
