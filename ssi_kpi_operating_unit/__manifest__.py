# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "HR - Key Perfomance Indicator (KPI) + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_kpi",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/kpi_employee.xml",
        "security/res_group/kpi_department.xml",
        "security/ir_rule/kpi_employee.xml",
        "security/ir_rule/kpi_department.xml",
        "view/kpi_employee.xml",
        "view/kpi_department.xml",
    ],
    "demo": [],
}
