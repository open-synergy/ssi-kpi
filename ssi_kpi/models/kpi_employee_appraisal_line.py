# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiEmployeeAppraisalLine(models.Model):
    """
    One appraiser's rating of a single KPI line on a
    ``kpi.employee_appraisal``. Concrete implementation of
    ``mixin.kpi_appraisal_line`` for the employee KPI.
    """

    _name = "kpi.employee_appraisal_line"
    _inherit = "mixin.kpi_appraisal_line"
    _description = "KPI Appraisal Line for Employee"

    kpi_appraisal_id = fields.Many2one(
        comodel_name="kpi.employee_appraisal",
    )
    kpi_line_id = fields.Many2one(
        comodel_name="kpi.employee_line",
    )
