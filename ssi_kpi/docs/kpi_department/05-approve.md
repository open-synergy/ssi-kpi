# Approve KPI for Department

> **Module:** ssi_kpi\
> **Model:** `kpi.department`\
> **Menu:** Human Resource > KPI > Departments\
> **Actor:** user in group KPI Department — Validator, registered as the pending approver\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The active `policy.template` grants `approve_ok` to the pending approver.
- **Access:** User is registered as an approver on the approval level that is currently
  pending, and is in group _KPI Department — Validator_.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled (this model uses a single approval level), status
  automatically changes to **In Progress**. This transition is not a separate button
  click — it is triggered automatically right after the last required approval, through
  the model's `_after_approved_method` (equivalent to running the **Start** action).
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
