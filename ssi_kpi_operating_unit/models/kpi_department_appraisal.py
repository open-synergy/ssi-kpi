# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class KpiDepartmentAppraisal(models.Model):
    """
    Adds single operating unit scoping to department KPI appraisals.
    Links each ``kpi.department_appraisal`` record to the operating
    unit it belongs to, so it can be filtered and access-controlled
    per unit.
    """

    _name = "kpi.department_appraisal"
    _inherit = [
        "kpi.department_appraisal",
        "mixin.single_operating_unit",
    ]
