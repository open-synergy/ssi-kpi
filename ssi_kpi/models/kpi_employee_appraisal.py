# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiEmployeeAppraisal(models.Model):
    """
    Single appraiser's review of a ``kpi.employee`` document.
    Concrete implementation of ``mixin.kpi_appraisal`` for the
    employee KPI.
    """

    _name = "kpi.employee_appraisal"
    _inherit = "mixin.kpi_appraisal"
    _description = "KPI Appraisal for Employee"

    kpi_id = fields.Many2one(
        comodel_name="kpi.employee",
    )
    employee_id = fields.Many2one(
        string="Employee", comodel_name="hr.employee", related="kpi_id.employee_id"
    )
    line_ids = fields.One2many(
        comodel_name="kpi.employee_appraisal_line",
    )
