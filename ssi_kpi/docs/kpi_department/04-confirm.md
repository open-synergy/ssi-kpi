# Confirm KPI for Department

> **Module:** ssi_kpi
> **Model:** `kpi.department`
> **Menu:** Human Resource > KPI > Departments
> **Actor:** user in group *KPI Department — User*
> **State:** `draft` → `confirm`
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Total weight of the **Details** lines (`amount_weight`) equals 100%.
- **Config:** The active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (*KPI Department — User*).
- **Config:** The active `approval.template` for this model matches this record and has
  at least one approver group configured (*KPI Department — Validator*).
- **Access:** User is in group *KPI Department — User*.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- An approval record is created for the approver group defined by the approval
  template.
