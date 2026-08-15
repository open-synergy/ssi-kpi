# Re-Compute KPI for Employee

> **Module:** ssi_kpi
> **Model:** `kpi.employee`
> **Menu:** Human Resource > KPI > Employees
> **Actor:** user in group *KPI Employee — User*
> **State:** `open` → `open`
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress** — the **Compute** button is only shown in this
  status.
- **Access:** User is in group *KPI Employee — User*.

## Flow

1. Open the **Human Resource > KPI > Employees** menu.
2. Open the record to recompute.
3. On the **Details** tab, click the **Compute** button.

## Post-Condition

- Realization, score, final score, and result (`kpi_result`) are recomputed for every
  line in the **Details** tab, and the **Total Weight(%)**/**Total Final Score(%)**
  footer totals are refreshed accordingly.
- Status remains **In Progress**.
