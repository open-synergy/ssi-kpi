# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiDepartmentAppraisal(models.Model):
    """
    Single appraiser's review of a ``kpi.department`` document.
    Concrete implementation of ``mixin.kpi_appraisal`` for the
    department KPI.
    """

    _name = "kpi.department_appraisal"
    _inherit = "mixin.kpi_appraisal"
    _description = "KPI Appraisal for Department"

    kpi_id = fields.Many2one(
        comodel_name="kpi.department",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        related="kpi_id.department_id",
    )
    line_ids = fields.One2many(
        comodel_name="kpi.department_appraisal_line",
    )
