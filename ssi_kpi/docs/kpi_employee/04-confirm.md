# Confirm KPI for Employee

> **Module:** ssi_kpi
> **Model:** `kpi.employee`
> **Menu:** Human Resource > KPI > Employees
> **Actor:** user in group *KPI Employee — User*
> **State:** `draft` → `confirm`
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Total weight of the **Details** lines (`amount_weight`) equals 100%.
- **Config:** The active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (*KPI Employee — User*).
- **Config:** The active `approval.template` for this model matches this record and has
  at least one approver group configured (*KPI Employee — Validator*).
- **Access:** User is in group *KPI Employee — User*.

## Flow

1. Open the **Human Resource > KPI > Employees** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- An approval record is created for the approver group defined by the approval
  template.
