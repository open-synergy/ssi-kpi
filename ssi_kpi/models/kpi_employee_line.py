# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiEmployeeLine(models.Model):
    """
    Single KPI item measured on a ``kpi.employee`` document. Concrete
    implementation of ``mixin.kpi_line`` for the employee KPI.
    """

    _name = "kpi.employee_line"
    _inherit = "mixin.kpi_line"
    _description = "KPI Line for Employee"

    kpi_id = fields.Many2one(
        comodel_name="kpi.employee",
    )
    score_range_ids = fields.One2many(
        string="Score Ranges",
        comodel_name="kpi.employee_line_score_range",
        inverse_name="kpi_line_id",
    )
