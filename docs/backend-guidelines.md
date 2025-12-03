# ActiFlow Backend 開發守則 v1

本文件定義 ActiFlow Backend 的後端開發規範，包含資料模型、Schema、CRUD、Router、RBAC 權限規則與程式風格。  
所有後續開發、修改、重構請一律遵守本守則，以維持專案結構一致性。

---

## 0. 使用方式（給開發者＋給 ChatGPT）

每次需要讓 AI 協助修改後端程式時，建議加上：

> 請嚴格依照「ActiFlow Backend 開發守則」產生 / 修改程式碼，欄位命名、schema、model、CRUD、router 都要保持一致。

---

## 1. 專案架構原則

### Backend Stack
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL**
- **Pydantic v2**
- **主體實體**
  - User（一般使用者 / 平台帳號）
  - SuperAdmin（平台 root）
  - SystemMembership（platform-level 權限：system_admin / support / auditor）
  - Organizer（主辦單位）
  - OrganizerMembership（organizer-level 角色：owner / admin / member）
  - ActivityTemplate / Event / Submission / SubmissionValue（之後的活動與表單）
- **分層原則**
  - models/：只放資料庫結構 + relationship，不放商業邏輯
  - schemas/：Pydantic 定義 API 收入/輸出
  - crud/：資料存取（CRUD），不放權限、業務判斷
  - core/：config、db、jwt、security、dependencies（權限依賴）
  - api/：router，每個領域有自己的檔案 / 目錄

---

## 2. SQLAlchemy Model 規則

### 2.1 Table / Model 命名
- Table：**複數 snake_case**
  - `users`, `organizers`, `system_memberships`
- Model：**單數 PascalCase**
  - `User`, `Organizer`, `SystemMembership`

### 2.2 必備共用欄位（BaseModel）

所有主表 Model 需繼承 `BaseModel`（專案既有），包含：

- id: int PK
- uuid: str API 對外主鍵
- is_active: bool = True
- is_deleted: bool = False
- created_at, updated_at, deleted_at
- created_at, updated_at, deleted_at: DateTime
- created_by, updated_by, deleted_by: String (通常存 user.uuid 或 super_admin.uuid)
- created_by_role, updated_by_role, deleted_by_role: String，例如：
  - "super_admin", "system_admin", "organizer", "user"

👉 規則：只要是業務主表，都應該繼承 BaseModel，沿用這組欄位。

❗ **Model 務必保持一致，不得自行新增不同命名風格的欄位。**

---

## 3. Pydantic Schema 規範

以 `User` 為例：

- `UserBase`：回傳共用欄位
- `UserCreate`：新增使用欄位，不含 uuid / timestamps
- `UserUpdate`：部分更新。所有欄位 Optional
- `UserResponse`：回傳型態（繼承 Base）

### Schema 命名規則（所有 Model 都遵循）
- XBase
- XCreate
- XUpdate
- XResponse

### 密碼欄位規則
- `password_hash` **不得出現在任何 Response schema**
- `password` / `old_password` / `new_password` 才是 API 使用欄位

---

## 4. CRUD 規則（app/crud/*.py）

CRUD 僅負責資料存取，不處理權限邏輯。

### CRUD 函式命名
- create_xxx(db, data)
- get_xxx_by_uuid(db, uuid)
- list_xxx(db, skip, limit)
- update_xxx(db, uuid, data)
- soft_delete_xxx(db, uuid)



### 特殊管理功能（只供 super_admin）
```shell
force_reset_password(db, uuid, new_password)
disable_user_account(db, uuid)
```

❗ **CRUD 不做權限判斷，不處理登入者資訊。**

---

## 5. Router 規則（app/api）

### Router 檔案結構
- app/api/auth/user_auth.py → /auth/users
- app/api/auth/organizer_auth.py → /auth/organizers
- app/api/auth/super_admin_auth.py → /auth/super-admin
- app/api/admin/super_admin_tools.py → /admin/super-tools
- app/api/system/system_users.py → /system/users


### 常見路由
#### User Auth：
- POST /auth/users/register
- POST /auth/users/login
- GET /auth/users/me
- PUT /auth/users/me
- POST /auth/users/change-password

#### Super Admin Tools：
- POST /admin/super-tools/users/{uuid}/force-reset-password
- POST /admin/super-tools/users/{uuid}/disable

---

## 6. RBAC 權限規則（dependencies.py）

ActiFlow 使用三層 RBAC：

1. **平台等級（SystemMembership）**  
   - system_admin  
   - support  
   - auditor  

2. **主辦單位等級（OrganizerMembership）**  
   - owner  
   - admin  
   - member  

3. **Super Admin（root）**

所有權限檢查集中在 `app/core/dependencies.py`。

### 6.1 Current User

```py
def get_current_user(...)
```

### 6.2 SuperAdmin 專用
```py
def get_current_super_admin(...)
```

### 6.3 Platform-level
```py
def get_current_platform_user
def get_current_system_admin
def get_current_support
def get_current_auditor
```

### 6.4 Organizer-level (factory)
```py
def get_current_organizer_admin_factory()
```

使用方式：

```py
@router.get("/organizers/{organizer_uuid}/xxx")
def list_items(
    organizer_uuid: str,
    admin = Depends(get_current_organizer_admin_factory())
):
```

### 7. Error Handling 規則
> 400 Bad Request
  - Email 重複
  - 密碼錯誤
  - 帳號需用第三方登入

> 401 Unauthorized
  - Token 遺失或無效
  - token 缺少 sub

> 403 Forbidden
  - 權限不足
  - 非 owner/admin 嘗試操作 organizer

> 404 Not Found
  - User / Organizer / Event 不存在

### 8. Alembic 規則
不得修改舊 Migration
如需更動 DB 結構 → 新增 migration：

```bash
alembic revision --autogenerate -m "add event fields"
alembic upgrade head
```

### 9. Commit / Branch 命名建議
```makefile

feat: add organizer auth
fix: system admin dependency
refactor: extract dependencies for RBAC
chore: update .gitignore
```

### 10. 三句最重要的守則
- ① 所有 Model 必須繼承 BaseModel，保持相同欄位（uuid / is_active / timestamps / created_by...）
- ② Schema 必須依照 Base / Create / Update / Response 命名，回傳絕不包含 password_hash
- ③ 任何權限檢查都必須使用 dependencies.py，不得在 router 裡自行寫 if 判斷


（完）


