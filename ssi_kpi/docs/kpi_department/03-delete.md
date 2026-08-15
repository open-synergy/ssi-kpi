# Delete KPI for Department

> **Module:** ssi_kpi\
> **Model:** `kpi.department`\
> **Menu:** Human Resource > KPI > Departments\
> **Actor:** user in group KPI Department — User\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User is in group _KPI Department — User_.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- The record is permanently removed from the system.
