# Edit KPI for Department

> **Module:** ssi_kpi
> **Model:** `kpi.department`
> **Menu:** Human Resource > KPI > Departments
> **Actor:** user in group *KPI Department — User*
> **Requires:** `01-create`
> **Inline Actions:** `action_populate_kpi` (Populate)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group *KPI Department — User*.

## Flow

1. Open the **Human Resource > KPI > Departments** menu.
2. Find and open the record to edit.
3. Click the **Edit** button, if the record is displayed as read-only. **(14.0)**
4. Change the required fields (**Department**, **Date Start**, **Date End**,
   **Template**).
5. On the **Details** tab, click **Populate** to rebuild the **Details** lines and the
   **Appraisals** list (`user_ids`) from the **Template** — for example after changing
   which **Template** is selected. Existing lines are discarded and replaced. You may
   also edit the **Details** lines manually instead. Skipping this step leaves the
   **Details** tab unchanged, which may no longer match the selected **Template**.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
