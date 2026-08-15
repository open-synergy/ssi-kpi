# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class KpiEmployeeAppraisal(models.Model):
    """
    Adds single operating unit scoping to employee KPI appraisals.
    Links each ``kpi.employee_appraisal`` record to the operating
    unit it belongs to, so it can be filtered and access-controlled
    per unit.
    """

    _name = "kpi.employee_appraisal"
    _inherit = [
        "kpi.employee_appraisal",
        "mixin.single_operating_unit",
    ]
