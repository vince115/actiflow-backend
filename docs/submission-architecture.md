# ActiFlow — Submission Architecture

> 本文件定義 Submission 在 ActiFlow 系統中的資料模型分層、Schema 分工與 API 使用規則。
> 目標是：**public / internal / response 完全解耦，各司其職**，避免 schema 混用與責任不清。

---

## 一、Submission 的三個世界（核心概念）

```
Public World (匿名 / 使用者)
└─ 送出報名表單
   └─ field_key + value
   └─ 最小回傳

Internal World (系統 / 後台)
└─ 真實資料結構
   └─ uuid / FK / status / audit
   └─ 完整 submission_values

Response World (對外輸出)
└─ 依角色裁切後的 view
   └─ public response
   └─ organizer / admin response
```

---

## 二、Schema 分類總覽

### 1️⃣ Public Submission（對外報名）

**用途**：匿名或已登入使用者送出活動報名
**設計原則**：

* 不暴露 DB 結構
* 不允許控制 status
* 不使用 uuid

#### 檔案位置

```
app/schemas/submission/submission_public.py
```

### SubmissionPublicCreate（Public Create Input）

```python
class SubmissionPublicCreate(BaseModel):
    user_email: EmailStr
    values: List[SubmissionValuePublicCreate]
    notes: Optional[str]
    extra_data: Optional[Dict[str, Any]]
```

### SubmissionValuePublicCreate

```python
class SubmissionValuePublicCreate(BaseModel):
    field_key: str
    value: Any
```

> ✔ 前端只知道 field_key
> ❌ 永遠不知道 event_field_uuid

---

### SubmissionPublicCreateResponse（Public Create Output）

**用途**：Public Create API 回傳（極簡）

```json
{
  "uuid": "...",
  "submission_code": "EVT-20251224-001",
  "status": "pending"
}
```

* ✔ 不回傳 values
* ✔ 不回傳 event_field 結構

---

## 三、Internal Submission（系統內部結構）

**用途**：DB / CRUD / Flow / Admin

### Model 結構

```
app/models/submission/
├── submission.py
├── submission_value.py
└── submission_file.py
```

### Submission（主檔）

* uuid
* submission_code
* event_uuid
* user_uuid / user_email
* status
* notes / extra_data
* audit fields

### SubmissionValue

* uuid
* submission_uuid (FK)
* event_field_uuid (FK)
* field_key（冗餘但必要）
* value (JSONB)
* files（附件）

> ⚠️ event_field_uuid **只存在於 internal**，public 世界永遠不知道

---

## 四、Internal Create（系統 / 後台使用）

### Schema 檔案

```
app/schemas/submission/submission_create.py
```

### SubmissionCreate

```python
class SubmissionCreate(BaseModel):
    event_uuid: UUID
    user_email: EmailStr
    user_uuid: Optional[UUID]
    values: List[SubmissionValueCreate]
    status: Optional[str] = "pending"
    notes: Optional[str]
    extra_data: Optional[Dict[str, Any]]
```

* ✔ 可指定 status
* ✔ 可指定 user_uuid
* ❌ 不可用於 public API

---

## 五、Response Schemas（回傳視角）

### Organizer / Admin Response

#### 檔案

```
app/schemas/submission/submission_response.py
```

### SubmissionResponse

```python
class SubmissionResponse(SubmissionBase):
    uuid: UUID
    user_name: Optional[str]
    user_email: Optional[str]
    values: List[SubmissionValueResponse]
```

* ✔ 完整 submission + values
* ✔ 後台使用
* ❌ 不給 public

---

## 六、API × Schema 對照表

| API                                          | Input Schema           | Output Schema                  |
| -------------------------------------------- | ---------------------- | ------------------------------ |
| POST /public/events/{event_uuid}/submissions | SubmissionPublicCreate | SubmissionPublicCreateResponse |
| GET /public/me/submissions（未來）               | –                      | SubmissionPublic               |
| POST /organizer/submissions（未來）              | SubmissionCreate       | SubmissionResponse             |
| GET /organizer/submissions                   | –                      | SubmissionResponse[]           |
| GET /admin/submissions                       | –                      | SubmissionResponse[]           |

---

## 七、核心鐵律（非常重要）

### field_key → event_field_uuid 轉換規則

> **此轉換只能發生在 API layer**

* ❌ 不在 schema
* ❌ 不在 model
* ❌ 不在 frontend

正確做法（範例）：

```python
field_map = {f.field_key: f for f in fields}
```

---

## 八、結論

* Public / Internal / Response 已完全解耦
* Schema 責任明確
* 架構可長期擴充（Flow / Approval / Payment）

**此 Submission 架構可作為 ActiFlow 長期穩定基礎。**
