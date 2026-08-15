# Create KPI for Employee

> **Module:** ssi_kpi
> **Model:** `kpi.employee`
> **Menu:** Human Resource > KPI > Employees
> **Actor:** user in group *KPI Employee — User*
> **State:** `—` → `draft`
> **Inline Actions:** `action_populate_kpi` (Populate)

## Pre-Condition

- **Data:** An active `kpi_template` record exists with **Type** *Employee* or *Both* —
  used by the **Populate** action to fill the **Details** tab.
- **Access:** User is in group *KPI Employee — User*.

## Flow

1. Open the **Human Resource > KPI > Employees** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Employee**: Automatically filled from the current user's own employee record, if
     one exists. Otherwise, select the employee this KPI record is for.
   - **Date Start** *(required)*: Start date of the evaluation period.
   - **Date End** *(required)*: End date of the evaluation period.
   - **Template**: Select the `kpi_template` to use. Optional, but required before
     **Populate** (step 4) can fill the **Details** tab.
4. On the **Details** tab, click **Populate** to rebuild the **Details** lines and the
   **Appraisals** list (`user_ids`) from the selected **Template**, and to copy its
   **Score Category**. Existing lines are discarded and replaced. You may also add lines
   to the **Details** tab manually instead of using this button. Skipping this step
   leaves the **Details** tab empty, which blocks **Confirm** — the total line weight
   must equal 100%.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
