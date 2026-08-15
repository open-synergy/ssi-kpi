# Restart KPI for Employee

> **Module:** ssi_kpi
> **Model:** `kpi.employee`
> **Menu:** Human Resource > KPI > Employees
> **Actor:** user in group *KPI Employee — Validator*
> **State:** `cancel` | `reject` → `draft`
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Reject**.
- **Config:** The active `policy.template` grants `restart_ok` for that state to the
  actor's group (*KPI Employee — Validator*).
- **Access:** User is in group *KPI Employee — Validator*.

## Flow

1. Open the **Human Resource > KPI > Employees** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
