<!-- docs/submission-architecture.md -->
# ActiFlow — Submission Architecture

本文件說明 ActiFlow 系統中 **Submission（報名資料）** 的整體架構設計，
包含資料分層（public / internal / response）、API 與 schema 對應、
以及報名流程中 Email 驗證的角色定位。

---

## 0. 本文件目的

* 說清楚 Submission 是什麼、不包含什麼
* 明確區分 Public / Internal / Response schema
* 避免未來擴充（金流、審核、模板版本）時再次混亂
* 作為後端、前端、未來維護者的共同契約文件

---

## 1. Submission 的三個世界（核心觀念）

Submission 在 ActiFlow 中同時存在於三個不同語境：

| 世界       | 說明                      |
| -------- | ----------------------- |
| Public   | 未登入或一般使用者送出報名           |
| Internal | 系統 / 後台建立或處理 Submission |
| Response | 後台 / 管理者查詢與顯示           |

**原則：三者永遠不共用同一個 schema**

---

## 2. Submission Lifecycle（狀態流程）

```
[填寫表單]
     ↓
pending                （已送出，尚未驗證）
     ↓
email_verified          （Email 驗證完成）
     ↓
paid                    （金流完成）
     ↓
completed               （報名成立）
     ↓
cancelled               （報名取消）
     ↓
[後續流程：金流 / 審核 / 取消]
```

### 設計原則

* Public API 只能建立 `pending`
* Email 驗證成功後，由系統更新狀態
* 「送出表單」≠「報名成立」


### Submission Status Lifecycle
⚠ confirmed is a business concept, not a Submission status.

pending
→ email_verified
→ paid
→ completed

All transitions are enforced by backend services.
Direct status mutation is forbidden.

### Cancellation (Out of Scope for Submission Status)

Cancellation is not represented as a Submission status.

A submission may be cancelled:
- before payment
- or after payment with refund logic

Cancellation is handled via:
- business rules
- audit records
- payment / refund workflows

Submission status remains immutable once completed.


---

## 3. Schema 分層設計

### 3.1 Public Schemas（前台）

**位置**
`app/schemas/submission/submission_public.py`

### SubmissionPublicCreate（前台送出）

```python
class SubmissionPublicCreate(BaseModel):
    user_email: EmailStr
    values: List[SubmissionValuePublicCreate]
    notes: Optional[str]
    extra_data: Optional[Dict[str, Any]]
```

設計重點：

* 不暴露 `field_uuid`
* 不允許指定 status
* 不包含 created_by / role
* 僅接受 `field_key + value`

---

### SubmissionPublic（前台查詢）

```python
class SubmissionPublic(BaseModel):
    submission_uuid: UUID
    event_uuid: UUID
    status: str
    submitted_at: datetime | None
    values: List[SubmissionValuePublic]
```

用途：

* `/me/submissions`
* 使用者查看自己的報名紀錄

---

## 3.2 Internal Schemas（系統 / 後台）

**位置**
`app/schemas/submission/submission_create.py`

```python
class SubmissionCreate(BaseModel):
    event_uuid: UUID
    user_email: EmailStr
    user_uuid: Optional[UUID]
    values: List[SubmissionValueCreate]
    notes: Optional[str]
    extra_data: Optional[Dict[str, Any]]
```

用途：

* 系統流程
* Admin / Organizer 建立 Submission
* 批次匯入 / 測試用途

---

## 3.3 Response Schemas（後台回傳）

**位置**
`app/schemas/submission/submission_response.py`

```python
class SubmissionResponse(SubmissionBase):
    uuid: UUID
    user_name: Optional[str]
    user_email: Optional[str]
    values: List[SubmissionValueResponse]
```

用途：

* Organizer / Admin 後台
* 包含完整 DB 欄位與關聯資料

---

## 4. SubmissionValue 設計原則

### Public Create（前台）

```python
class SubmissionValuePublicCreate(BaseModel):
    field_key: str
    value: Any
```

### Internal / DB

```python
class SubmissionValue(BaseModel):
    submission_uuid
    event_field_uuid
    field_key
    value (JSONB)
```

### 鐵律（非常重要）

**field_key → field_uuid 的轉換，只能發生在 API layer**

* 不在 schema
* 不在 model
* 不在前端
* 僅在 API

---

## 5. API × Schema 對照表

| API                                            | 用途    | Request Schema         | Response Schema                |
| ---------------------------------------------- | ----- | ---------------------- | ------------------------------ |
| POST `/public/events/{event_uuid}/submissions` | 前台報名  | SubmissionPublicCreate | SubmissionPublicCreateResponse |
| GET `/me/submissions`                          | 使用者查詢 | -                      | SubmissionPublic               |
| POST `/admin/submissions`                      | 後台建立  | SubmissionCreate       | SubmissionResponse             |
| GET `/admin/submissions/{uuid}`                | 後台查看  | -                      | SubmissionResponse             |

---

## 6. Email 驗證流程（流程層）

### 為什麼 Email 驗證不屬於 Submission？

* Submission 是資料
* Email 驗證是流程控制

### 責任分離

| 項目       | 負責者        |
| -------- | ---------- |
| Token 產生 | 後端         |
| Email 發送 | 後端         |
| 點擊驗證     | 使用者        |
| 狀態更新     | Verify API |

### 建議 API

* `POST /auth/email-verification/send`
* `POST /auth/email-verification/verify`

---

## 7. Email 為什麼一定由後端發送？

* 前端不能保存 SMTP / API Key
* 防止偽造驗證信
* 可隨時切換 Email Provider（SES / Resend / SendGrid）

前端只負責觸發，後端負責發送。

---

## 8. 總結（定版規格）

* Submission 有三個世界
* Public / Internal / Response 永不混用
* field_key 是 UX，uuid 是 DB
* Email 驗證是流程，不是資料
* 本文件為 Submission 架構定版文件
