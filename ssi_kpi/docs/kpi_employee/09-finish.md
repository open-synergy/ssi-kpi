# Finish KPI for Employee

> **Module:** ssi_kpi
> **Model:** `kpi.employee`
> **Menu:** Human Resource > KPI > Employees
> **Actor:** user in group *KPI Employee — User*
> **State:** `open` → `done`
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Record:** Every record in the **Appraisals** tab (`appraisal_ids`) has status
  **Done**. **Done** is blocked otherwise.
- **Config:** The active `policy.template` grants `done_ok` for state `open` to the
  actor's group (*KPI Employee — User*).
- **Access:** User is in group *KPI Employee — User*.

## Flow

1. Open the **Human Resource > KPI > Employees** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
- Realization, score, final score and result are recomputed automatically.
