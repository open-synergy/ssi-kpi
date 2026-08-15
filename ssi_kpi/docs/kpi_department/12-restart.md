# Restart KPI for Department

> **Module:** ssi_kpi
> **Model:** `kpi.department`
> **Menu:** Human Resource > KPI > Departments
> **Actor:** user in group *KPI Department — Validator*
> **State:** `cancel` | `reject` → `draft`
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Reject**.
- **Config:** The active `policy.template` grants `restart_ok` for that state to the
  actor's group (*KPI Department — Validator*).
- **Access:** User is in group *KPI Department — Validator*.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
