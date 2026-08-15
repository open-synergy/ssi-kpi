# Create KPI for Department

> **Module:** ssi_kpi_operating_unit
> **Extends:** ssi_kpi — model `kpi.department`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one field:

- **Operating Unit**: The operating unit this KPI record belongs to. Optional.
  Defaults to the user's default operating unit. Only visible to users in the
  _Manage Multi Operating Unit_ group.

## Modified — Record Visibility

- The Departments list is now filtered by operating unit (record rule). A user
  in the _Operating Unit_ data ownership group only sees records of operating
  units they are assigned to. This is not a Flow step.
