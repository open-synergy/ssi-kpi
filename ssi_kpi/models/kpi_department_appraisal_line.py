# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiDepartmentAppraisalLine(models.Model):
    """
    One appraiser's rating of a single KPI line on a
    ``kpi.department_appraisal``. Concrete implementation of
    ``mixin.kpi_appraisal_line`` for the department KPI.
    """

    _name = "kpi.department_appraisal_line"
    _inherit = "mixin.kpi_appraisal_line"
    _description = "KPI Appraisal Line for Department"

    kpi_appraisal_id = fields.Many2one(
        comodel_name="kpi.department_appraisal",
    )
    kpi_line_id = fields.Many2one(
        comodel_name="kpi.department_line",
    )
