# Terminate KPI for Department

> **Module:** ssi_kpi\
> **Model:** `kpi.department`\
> **Menu:** Human Resource > KPI > Departments\
> **Actor:** user in group KPI Department — User\
> **State:** `open` → `terminate`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Config:** The active `policy.template` grants `terminate_ok` for state `open` to the
  actor's group (_KPI Department — User_).
- **Access:** User is in group _KPI Department — User_.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Open the record to terminate.
3. Click the **Terminate** button.
4. In the wizard that appears, select the **Termination Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Terminate**.
