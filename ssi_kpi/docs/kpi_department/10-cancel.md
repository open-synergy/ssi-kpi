# Cancel KPI for Department

> **Module:** ssi_kpi
> **Model:** `kpi.department`
> **Menu:** Human Resource > KPI > Departments
> **Actor:** user in group *KPI Department — Validator*
> **State:** `draft` | `confirm` | `open` | `done` | `terminate` → `cancel`
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **In Progress**, **Done**,
  or **Terminate**.
- **Record:** No record in the **Appraisals** tab (`appraisal_ids`) has status **Done**
  — **Cancel** is blocked otherwise.
- **Config:** The active `policy.template` grants `cancel_ok` for that state to the
  actor's group (*KPI Department — Validator*).
- **Access:** User is in group *KPI Department — Validator*.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- All records in the **Appraisals** tab (`appraisal_ids`) are removed.
