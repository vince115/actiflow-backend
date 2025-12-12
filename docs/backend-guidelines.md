# **ActiFlow Backend 開發守則 v2

（完整正式版 / 2025-12 最新架構）**

本文件定義 ActiFlow Backend 的開發規範，用於維護 API 架構一致性、資料模型完整性、RBAC 行為統一性，以及 router / CRUD / schema 的標準命名方式。

所有後端開發必須遵守本文件。

## #️⃣ 1. Backend 技術架構（Tech Stack）

| 類別 | 工具 |
| ---------- | ---------- |
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| DB | PostgreSQL（Neon） |
| Migrations | Alembic |
| Schema | Pydantic v2 |
| Auth | Cookie-Based JWT（HttpOnly） |
| RBAC | Decorator-based（require_xxx_role） |
| Deployment  | Docker / Cloud Run |

## #️⃣ 2. 目錄結構（必須遵循 DDD Domain-Based）
```pgsql
app/
  api/
    activities/
    admin/
    applications/
    auth/
    events/
    organizers/
    submissions/
    system/
    users/
    utils/
    router.py         ← ⭐ 全域路由匯總

  core/
    config.py
    db.py
    dependencies.py
    jwt.py
    security.py
    rbac.py
    exceptions.py

  models/
    activity/
    auth/
    base/
    event/
    membership/
    organizer/
    platform/
    submission/
    user/

  schemas/
    activity/
    auth/
    event/
    membership/
    organizer/
    platform/
    submission/
    user/
    shared/

  crud/
    activity/
    auth/
    event/
    membership/
    organizer/
    submission/
    user/
    platform/

  utils/
    logging.py
    email.py
```

## #️⃣ 3. Model 規範（SQLAlchemy）

所有主資料表 必須繼承 BaseModel（企業級審計欄位）：

### ✔ BaseModel 必含欄位：
```python
id
uuid
is_active
is_deleted

created_at
updated_at
deleted_at

created_by
updated_by
deleted_by

created_by_role
updated_by_role
deleted_by_role
```
### ✔ 命名規則
| 類型	| 命名 |
| ---------- | ---------- |
| 主表	| activity_template.py, event.py, submission.py
| 附表	| activity_template_field.py, event_ticket.py

### ❌ 禁止

不可將 Activity 與 Event 放同一資料夾

不可出現 business logic

## #️⃣ 4. Schema 命名規範（Pydantic v2）

所有 Schema 必須由以下四組構成：

| Schema | 用途 |
| ---------- | ---------- |
| XBase | 共用欄位（R/O） |
| XCreate | 建立用 |
| XUpdate | 部分更新 |
| XResponse | 回傳用（不可含密碼相關欄位） |

### ✔ Schema Example（必須遵守）
```python
class UserBase(BaseModel):
    uuid: UUID
    name: str
    email: EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

class UserResponse(UserBase):
    created_at: datetime
```

### ❌ 禁止

password_hash 不能出現在任何 Response

混合使用 Create/Update 在同檔案

## #️⃣ 5. CRUD 規範（資料存取層）

CRUD 層 禁止放置任何 RBAC / Auth / Router Logic。

每個 domain 拆分成多檔案，如：
```bash
crud/activity/activity.py
crud/activity/activity_template.py
crud/activity/activity_template_field.py
```

### ✔ CRUD 函式命名規則
```nginx
create_xxx
get_xxx_by_uuid
get_xxx_by_email
list_xxx
update_xxx
soft_delete_xxx
```

### SuperAdmin 專用（只在 user CRUD）

```nginx
force_reset_password
disable_user_account
```

## #️⃣ 6. Router 規範（API Domain 分層）

ActiFlow 採用 Domain-Based Router + Multi-Role Endpoints。

### Router 目錄規範（必須遵循）：
```pgsql
api/
  activities/
  events/
  organizers/
  submissions/
  applications/
  admin/
  system/
  auth/
  users/
  utils/
```

### API 必須分 4 類 Role：

| 類型 | 目錄 | 說明 |
| ---------- | ---------- | ---------- |
| public | events_public.py / submissions_public.py | 使用者可瀏覽 |
| organizer | events_organizer.py | 主辦單位後台 |
| admin | admin/ | 平台管理後台 |
| system | system/ | 超級管理員 |

### ✔ 禁止的舊檔案（必須刪除）
```nginx
user_auth.py
organizer_auth.py
super_admin_auth.py
system_auth.py
```

## #️⃣ 7. 新版 Auth 規範（Cookie-Based JWT）

### ✔ 採用 HttpOnly Cookies：
|Cookie|用途|
|----------|----------| 
|access_token|15–30 分鐘存活|
|refresh_token|7–14 天存活|

### ✔ 4 個 Auth API（必須存在）
|路由|	說明|
|----------|----------| 
|POST /auth/login|登入（設置 cookies）|
|POST /auth/refresh|更新 access token|
|GET /auth/me|取得當前使用者|
|POST /auth/logout|清除 cookies|

### ❌ 禁止使用：

- OAuth2PasswordBearer
- Authorization: Bearer <token>

## #️⃣ 8. RBAC（新版 Role-Based Access Control）

ActiFlow 採用 decorator RBAC（建議方式）：

```python
@require_super_admin
@require_platform_role("system_admin")
@require_organizer_role(["owner", "admin"])
```


Base dependency：
```python
current_user = Depends(get_current_user)
```

### ✔ 不再使用：
```python
get_current_super_admin()
get_current_system_admin()
get_current_organizer_admin_factory()
```

## #️⃣ 9. Router / Prefix / Tags 規範

### ✔ Tags 必須依 Domain：

例：

```python
router = APIRouter(prefix="/events", tags=["Events"])
```

### ✔ 正式 endpoint 不得使用 /debug
Debug endpoint 改為：
 
```swift
api/utils/debug.py
router = APIRouter(prefix="/debug", tags=["Debug"], include_in_schema=False)
```


並且：
- 必須限制環境（DEV only）
- 上線時自動關閉

## #️⃣ 10. 錯誤回應規範
| HTTP Code	| 用法 |
|----------|----------| 
| 400	| 格式錯誤 / 驗證失敗 |
| 401	| 未登入 / Cookie 遺失 |
| 403	| 權限不足 |
| 404	| 資料不存在 |
| 409	| 重複建立（email、活動名稱等） |

## #️⃣ 11. Alembic 規範
### ✔ Migration 只能新增不可修改

```python
alembic revision -m "add event fields"
alembic upgrade head
```

### ❌ 禁止

修改已存在的 migration（會破壞 production 資料庫）

## #️⃣ 12. Git Commit 規範（必須遵守）

| Type	| Description |
|----------|----------| 
| feat	| 新功能 |
| fix	| 修复 bug |
| refactor	| 重构代码 |
| chore	| 构建过程或辅助工具的变动 |

例：

```python
feat: add activity template CRUD
fix: correct refresh token expiry logic
refactor: unify RBAC decorators
chore: cleanup old auth handlers
```

## #️⃣ 13. 最重要的三點（請背下）

### ① Auth 改為 Cookie-Based，不能出現 Bearer Token

### ② RBAC 採 decorator，不使用 old get_current_xxx

### ③ Model / Schema / CRUD / Router 必須依規範命名與分類

## #️⃣ 14. 附錄：最終版 API Folder 樹狀圖（精簡）

```markdown
api/
  activities/
    activity_templates.py
    activity_template_fields.py
    activity_types.py

  events/
    events_public.py
    events_organizer.py
    events_admin.py
    event_fields.py
    event_template_fields.py

  organizers/
    organizers_public.py
    organizers_admin.py
    organizer_members.py
    organizer_events.py

  submissions/
    submissions_public.py
    submissions_organizer.py
    submissions_admin.py
    submission_values.py

  applications/
    organizer_applications_public.py
    organizer_applications_admin.py

  auth/
    login.py
    refresh.py
    logout.py
    me.py

  admin/
    organizers.py
    events.py
    submissions.py
    system_settings.py
    users.py
    tools.py

  system/
    system_auth.py
    system_users.py
    system_memberships.py
    organizer_approval.py

  users/
    users_public.py

  utils/
    debug.py

  router.py
```
### 🎉 Done!