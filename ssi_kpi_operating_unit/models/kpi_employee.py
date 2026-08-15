# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class KpiEmployee(models.Model):
    """
    Adds single operating unit scoping to employee KPI documents.
    Links each ``kpi.employee`` record to the operating unit it
    belongs to, so it can be filtered and access-controlled per unit.
    """

    _name = "kpi.employee"
    _inherit = [
        "kpi.employee",
        "mixin.single_operating_unit",
    ]
