# WORKING_MODEL_AUTH_USER_MEMBERSHIP_v0.2

> ActiFlow Backend  
> Auth / User / Membership Working Model  
> Version: v0.2  
> Status: ✅ Verified & Stable  
> Last updated: 2025-12-18

---

### 🎯 Purpose

本文件定義 **ActiFlow Backend** 中已被實際驗證、可長期使用的核心帳號模型，涵蓋：

- Auth（登入與身份驗證）
- User（使用者本體）
- Membership（System / Organizer 身分）
- `/auth/me` 聚合回傳模型

本文件描述的是 **「已實際跑通的工作模型（Working Model）」**，  
不是設計草稿，也不是理論提案。

---

###  🧠 Core Design Principles

### 1. User ≠ Role
- `User` 只是登入主體
- **權限永遠不直接掛在 User 上**
- 權限來自 Membership（System / Organizer）

### 2. Membership is Polymorphic
- 系統存在多種 membership 類型
- 透過 `type` discriminator 做多型聚合
- `/auth/me` 是 **Aggregator API**

### 3. Cookie-based JWT
- 使用 HttpOnly Cookie
- 不使用 Authorization Header
- `/auth/me` 僅依賴 cookie 驗證身份

---

### 🔐 Auth Model (Verified)

### POST `/auth/login`
- 驗證 email + password
- 成功後：
  - 寫入 HttpOnly cookie（access token）
  - 回傳 minimal user info

### GET `/auth/me`
- 從 cookie 解析 access token
- 回傳 User Public View + Memberships

---

### 👤 User Model

### users table（登入最低需求）
- `uuid`
- `email`
- `password_hash`
- `auth_provider = "local"`
- `is_email_verified`
- `config`
- `is_active`
- `is_deleted`

### User Public Schema
```json
{
  "uuid": "uuid",
  "email": "email",
  "name": null,
  "role": "user",
  "memberships": []
}
```
- role 為安全預設值 "user"
- 真正權限來自 memberships

---
### 🧩 Membership Model
#### Membership Base (Polymorphic Root)

```python
class MembershipBase(BaseModel):
    type: Literal["system", "organizer"]

    model_config = {"from_attributes": True}
```

- 所有 membership public schema 皆繼承此 base
- type 為 discriminator
- 支援 ORM → Schema 轉換

### 🔑 System Membership
#### system_memberships table

- user_uuid
- role
- is_active
- is_suspended
- config

### Public Schema
```json
{
  "type": "system",
  "role": "admin",
  "status": "active"
}
```

#### Status Mapping Rule

- is_suspended = true → "suspended"
- is_active = true → "active"
- 其他 → "inactive"

---

### 🏢 Organizer Membership
#### organizer_memberships table

- user_uuid
- organizer_uuid
- role
- is_active
- is_deleted

### Public Schema
```json
{
  "type": "organizer",
  "organizer_uuid": "uuid",
  "organizer_name": "Organizer Name",
  "membership_role": "owner"
}
```
### 🔗 /auth/me Aggregation Model
#### Response Schema

```json
{
  "uuid": "uuid",
  "email": "email",
  "name": null,
  "role": "user",
  "memberships": [
    {
      "type": "system",
      "role": "admin",
      "status": "active"
    }
  ]
}
```

Characteristics

同時回傳 System + Organizer memberships

使用 Union schema + discriminator

不在 /auth/me 做權限判斷（僅回傳資料）

🧠 Responsibility Boundaries
| Layer | 	Responsibility |
| ------ | ------ |
| Auth | 身份驗證、Token |
| User | 登入主體 |
| Membership |	身分與角色 |
| /auth/me | 資料聚合 |
| RBAC | 權限判斷（下一階段）|

🚦 Stability Contract

- ✅ 本模型已實際驗證
- ❌ 不應隨意修改 schema 結構
- ❌ 不應將 role 直接加回 User
- ✅ 新增 membership 類型時，應延伸 polymorphic model

🔜 Next Steps (Planned)

- RBAC helpers (require_system_role, require_organizer_role)
- Organizer-based permission enforcement
- Admin API access control

📌 Summary

> Auth / User / Membership v0.2
> 是 ActiFlow Backend 的 身份與權限基石，
> 所有後續 API 與 RBAC 設計皆應建立在此模型之上。


