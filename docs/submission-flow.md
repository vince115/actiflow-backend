 <!-- docs/submission-flow.md -->

# Submission Flow & Status Lifecycle

本文件說明 ActiFlow 中 Submission（報名） 的完整生命週期，
包含 狀態轉換規則、API 對應、角色權限、以及 Email 通知行為。

## 1. Submission Status 定義
| Status |	說明 |
| --- |	--- |
| pending |	使用者已送出報名，但尚未驗證 Email |
| email_verified |	使用者已完成 Email 驗證 |
| paid |	使用者已完成付款 / 確認 |
| completed |	Organizer 已核准，報名完成 |
| rejected |	Organizer 已拒絕此報名 |

## 2. 狀態轉換規則（Domain Rule）

定義於：
app/crud/submission/crud_submission_status.py

```text
pending         → email_verified
email_verified  → paid
paid            → completed
paid            → rejected
completed       → paid        (reopen)
rejected        → paid        (reopen)
```

> ❗ 任何不在此表內的轉換都會拋出 InvalidSubmissionStatusTransition

## 3. API / Status / Email 對照表

### 3.1 Public Flow（使用者）

| API |	From → To |	Role |	Email |
| --- | --- | --- | --- |
| POST /public/events/{event_uuid}/submissions | — → pending | Public | ❌ |
| POST /public/events/submissions/{uuid}/confirm-email | pending → email_verified | Public | ❌ |
| POST /public/events/submissions/{uuid}/mark-paid | email_verified → paid | Public | ❌ |

### 3.2 Organizer Flow（主辦單位）

#### ✅ Approve（核准）

| API |	From → To |	Role |	Email |
| --- | --- | --- | --- |
| POST /organizer/{org_uuid}/events/{event_uuid}/submissions/{uuid}/approve	| paid → completed | Organizer Admin / Owner |	✅ completed |

#### 📧 Email：

- Template：submission_completed_email

- 通知報名者「報名已完成」

#### ❌ Reject（拒絕）

| API |	From → To |	Role |	Email |
| --- | --- | --- | --- |
| POST /organizer/{org_uuid}/events/{event_uuid}/submissions/{uuid}/reject | paid → rejected | Organizer Admin / Owner | ✅ rejected |

- 必填欄位：reason
- 儲存至：submission.status_reason

#### 📧 Email：

- Template：submission_rejected_email
- 內容包含 reject reason（對使用者可見）

🔄 Reopen（重新開啟）
| API |	From → To | Role |	Email |
| --- | ---| --- | --- |
| POST /organizer/{org_uuid}/events/{event_uuid}/submissions/{uuid}/reopen	| rejected / completed → paid	| Organizer Admin / Owner	| ✅ reopened |

### 行為說明：

1. 清空舊的 status_reason
2. 寫入 submission.notes（internal note）
3. 將狀態設回 paid

> 📧 Email：

- Template：submission_reopened_email
- 說明重新開啟原因（notes）

## 4. Notes vs Status Reason 說明

| 欄位 | 用途 | 對象 |
| --- | --- | --- |
| status_reason	| 官方狀態理由（例如 reject 原因） | 使用者可見 |
| notes	| 內部備註（reopen / admin 操作說明） | Organizer / Admin |

## 5. Email Notification 設計原則

- 所有 Email side effects 皆集中於：
```bash
app/services/submission/notification.py
```

- API 層只負責：

  - 狀態變更

  - try / except 呼叫 notification（不可影響主流程）

- Email Template 與邏輯分離：

```bash
app/api/utils/email_templates.py
app/api/utils/email_mailer.py
```
## 6. 設計原則摘要

- ✅ Domain rule 與 API 行為分離

- ✅ Side effects 不影響主交易流程

- ✅ Organizer 操作具備可逆性（reopen）

- ✅ Email 不寫死在 API


