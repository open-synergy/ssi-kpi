# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class KpiEmployee(models.Model):
    _name = "kpi.employee"
    _inherit = [
        "kpi.employee",
        "mixin.single_operating_unit",
    ]


class KpiEmployeeAppraisal(models.Model):
    _name = "kpi.employee_appraisal"
    _inherit = [
        "kpi.employee_appraisal",
        "mixin.single_operating_unit",
    ]
