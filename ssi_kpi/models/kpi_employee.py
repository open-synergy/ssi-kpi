# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class KpiEmployee(models.Model):
    """
    KPI evaluation document for an ``hr.employee``. Concrete
    implementation of ``mixin.kpi`` scoped to one employee per
    evaluation period.
    """

    _name = "kpi.employee"
    _inherit = "mixin.kpi"
    _description = "KPI for Employee"

    @api.model
    def _default_employee_id(self):
        """Default ``employee_id`` to the current user's first employee.

        :return: id of ``self.env.user.employee_ids[0]``, or ``None``
            if the current user has no linked employee
        """
        employees = self.env.user.employee_ids
        if len(employees) > 0:
            return employees[0].id

    kpi_template_id = fields.Many2one(
        domain="['|',('type', '=', 'employee'), ('type', '=', 'both')]"
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        default=lambda self: self._default_employee_id(),
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    line_ids = fields.One2many(
        comodel_name="kpi.employee_line",
    )
    appraisal_ids = fields.One2many(
        comodel_name="kpi.employee_appraisal",
    )

    def _check_overlap(self):
        """Check for another non-cancelled KPI overlapping this period.

        :return: ``False`` when another ``kpi.employee`` record for
            the same ``employee_id`` overlaps ``date_start``/
            ``date_end``, ``True`` otherwise
        """
        self.ensure_one()
        result = True
        criteria = [
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("employee_id", "=", self.employee_id.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]
        check = self.search_count(criteria)
        if check > 0:
            result = False

        return result
