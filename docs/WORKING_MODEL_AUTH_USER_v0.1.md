# Auth / User – Working Model v0.1（文件版）

### 1️⃣ 系統範圍（Scope）
ㄑ
本文件定義 ActiFlow Backend 中以下子系統的「事實模型」：
- Auth（登入 / session / token）
- Security（hash / jwt / middleware）
- User（使用者本體，不含權限）


不包含：
- RBAC 規則細節
- Organizer / System 權限判斷
- Event / Activity 模組

### 2️⃣ Environment 約束（硬性）
- 開發 / 測試環境：test DB（ep-misty-frog）
- Auth 架構：Cookie-based JWT
- ❌ 不使用 OAuth2PasswordBearer
- ❌ 不使用 Authorization: Bearer header

### 3️⃣ Auth API（已驗證）
🔹 POST /auth/login

輸入
```json
{
  "email": "string",
  "password": "string"
}
```

行為

- 驗證 email + password
- 僅支援 auth_provider = 'local'

成功後：

- 設定 HttpOnly cookie（access token）
- 回傳 minimal user info

成功回傳
```json 
{
  "success": true,
  "user": {
    "uuid": "uuid",
    "email": "email"
  }
}
```
#### 🔹 GET /auth/me

特性

- 不接受 Authorization header
- 僅從 cookie 解析 access token

成功回傳（實證結果）
```json
{
  "uuid": "uuid",
  "email": "email",
  "name": null,
  "role": "user",
  "memberships": []
}
```

#### 4️⃣ Security（硬性規範）
🔐 Password

- Hash API：hash_password(password: str)
- Verify API：verify_password(plain, hashed)
- Hash algorithm：bcrypt（由實作決定）

❌ 專案內 不存在 get_password_hash

🔐 JWT / Middleware

- Token 存放位置：HttpOnly Cookie
- Middleware：
  - 負責 decode token
  - 設定 current user context
- /auth/me 已實證可正確取回 user

### 5️⃣ User Model（DB 事實）
users table（登入必要欄位）
```text
uuid                  NOT NULL
email                 NOT NULL
password_hash          NOT NULL
auth_provider          NOT NULL ('local')
is_email_verified      NOT NULL
config                 NOT NULL (jsonb)
is_active              NOT NULL
is_deleted              NOT NULL
```

#### 語意約束

- User ≠ Role
- User 本身不代表任何權限
- 預設 role 回傳為 "user"（安全預設）

6️⃣ 重要結論（v0.1）

✅ Auth / Security / User 主線 已完成且被實證
✅ 可作為後續 RBAC / Membership 的穩定基礎
❌ 不應再修改 Auth 架構本身，除非版本升級


