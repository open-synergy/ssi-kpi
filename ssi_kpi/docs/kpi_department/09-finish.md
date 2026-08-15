# Finish KPI for Department

> **Module:** ssi_kpi
> **Model:** `kpi.department`
> **Menu:** Human Resource > KPI > Departments
> **Actor:** user in group *KPI Department — User*
> **State:** `open` → `done`
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Record:** Every record in the **Appraisals** tab (`appraisal_ids`) has status
  **Done**. **Done** is blocked otherwise.
- **Config:** The active `policy.template` grants `done_ok` for state `open` to the
  actor's group (*KPI Department — User*).
- **Access:** User is in group *KPI Department — User*.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
- Realization, score, final score and result are recomputed automatically.
