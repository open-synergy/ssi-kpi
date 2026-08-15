# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiDepartment(models.Model):
    """
    KPI evaluation document for a ``hr.department``. Concrete
    implementation of ``mixin.kpi`` scoped to one department per
    evaluation period.
    """

    _name = "kpi.department"
    _inherit = "mixin.kpi"
    _description = "KPI for Department"

    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    kpi_template_id = fields.Many2one(
        domain="['|',('type', '=', 'department'), ('type', '=', 'both')]"
    )
    line_ids = fields.One2many(
        comodel_name="kpi.department_line",
    )
    appraisal_ids = fields.One2many(
        comodel_name="kpi.department_appraisal",
    )

    def _check_overlap(self):
        """Check for another non-cancelled KPI overlapping this period.

        :return: ``False`` when another ``kpi.department`` record for
            the same ``department_id`` overlaps ``date_start``/
            ``date_end``, ``True`` otherwise
        """
        self.ensure_one()
        result = True
        criteria = [
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("department_id", "=", self.department_id.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]
        check = self.search_count(criteria)
        if check > 0:
            result = False

        return result
