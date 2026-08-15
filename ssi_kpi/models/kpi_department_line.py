# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiDepartmentLine(models.Model):
    """
    Single KPI item measured on a ``kpi.department`` document.
    Concrete implementation of ``mixin.kpi_line`` for the department
    KPI.
    """

    _name = "kpi.department_line"
    _inherit = "mixin.kpi_line"
    _description = "KPI Line for Department"

    kpi_id = fields.Many2one(
        comodel_name="kpi.department",
    )
    score_range_ids = fields.One2many(
        string="Score Ranges",
        comodel_name="kpi.department_line_score_range",
        inverse_name="kpi_line_id",
    )
