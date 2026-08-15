# Reject KPI for Department

> **Module:** ssi_kpi\
> **Model:** `kpi.department`\
> **Menu:** Human Resource > KPI > Departments\
> **Actor:** user in group KPI Department — Validator, registered as the pending approver\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The active `policy.template` grants `reject_ok` to the pending approver.
- **Access:** User is registered as an approver on the approval level that is currently
  pending, and is in group _KPI Department — Validator_.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Reject**.
