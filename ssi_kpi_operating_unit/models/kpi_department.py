# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class KpiDepartment(models.Model):
    _name = "kpi.department"
    _inherit = [
        "kpi.department",
        "mixin.single_operating_unit",
    ]


class KpiDepartmentAppraisal(models.Model):
    _name = "kpi.department_appraisal"
    _inherit = [
        "kpi.department_appraisal",
        "mixin.single_operating_unit",
    ]
