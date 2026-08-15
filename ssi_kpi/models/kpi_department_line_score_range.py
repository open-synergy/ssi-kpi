# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiDepartmentLineScoreRange(models.Model):
    """
    Score range bracket for a ``kpi.department_line``. Concrete
    implementation of ``mixin.kpi_line_score_range`` for the
    department KPI.
    """

    _name = "kpi.department_line_score_range"
    _inherit = "mixin.kpi_line_score_range"
    _description = "KPI Line for Department"

    kpi_line_id = fields.Many2one(
        comodel_name="kpi.department_line",
    )
