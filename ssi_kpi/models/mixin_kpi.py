# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ssi_decorator import ssi_decorator


class MixinKpi(models.AbstractModel):
    """
    Abstract base for a KPI evaluation document (draft/confirm/open/
    done). Populates its ``line_ids`` from a ``kpi_template``, collects
    per-user appraisals in ``appraisal_ids``, and aggregates weight,
    final score, and result category once appraisals are done.
    """

    _name = "mixin.kpi"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_terminate",
        "mixin.date_duration",
    ]
    _description = "Abstract Class for KPI"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False
    _automatically_insert_open_policy_fields = False

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "action_terminate",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_terminate",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    @api.model
    def _get_policy_field(self):
        """Extend the policy field list with this mixin's own fields.

        :return: list of policy field names inherited from the base
            mixin plus the KPI-specific policy fields
        """
        res = super(MixinKpi, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "terminate_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("reject", "Reject"),
            ("terminate", "Terminate"),
            ("cancel", "Cancelled"),
        ],
    )
    kpi_template_id = fields.Many2one(
        string="Template",
        comodel_name="kpi_template",
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    kpi_score_categ_id = fields.Many2one(
        string="Score Category",
        comodel_name="kpi_score_categ",
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    user_ids = fields.Many2many(
        string="Appraisals",
        comodel_name="res.users",
        column1="user_id",
        column2="kpi_id",
    )
    line_ids = fields.One2many(
        string="Details",
        comodel_name="mixin.kpi_line",
        inverse_name="kpi_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=True,
    )
    appraisal_ids = fields.One2many(
        string="Appraisal Lines",
        comodel_name="mixin.kpi_appraisal",
        inverse_name="kpi_id",
    )

    @api.depends(
        "line_ids",
        "line_ids.weight",
    )
    def _compute_amount_weight(self):
        """Sum ``weight`` across ``line_ids`` into ``amount_weight``."""
        for record in self:
            total_weight = 0.0
            for line in record.line_ids:
                total_weight += line.weight
            record.amount_weight = total_weight

    amount_weight = fields.Float(
        string="Total Weight(%)",
        store=True,
        readonly=True,
        compute="_compute_amount_weight",
    )

    @api.depends(
        "line_ids",
        "line_ids.final_score",
    )
    def _compute_amount_final_score(self):
        """Sum ``final_score`` across ``line_ids`` into the total."""
        for record in self:
            total_final_score = 0.0
            for line in record.line_ids:
                total_final_score += line.final_score
            record.amount_final_score = total_final_score

    amount_final_score = fields.Float(
        string="Total Final Score(%)",
        store=True,
        readonly=True,
        compute="_compute_amount_final_score",
    )

    @api.depends(
        "kpi_score_categ_id",
        "amount_final_score",
    )
    def _compute_kpi_result(self):
        """Resolve ``kpi_result`` from the score category range.

        Delegates to ``kpi_score_categ_id._get_range_result`` with
        ``amount_final_score``; empty when no category is set.
        """
        for record in self:
            result = ""
            if record.kpi_score_categ_id:
                result = record.kpi_score_categ_id._get_range_result(
                    record.amount_final_score
                )
            record.kpi_result = result

    kpi_result = fields.Char(
        string="Result",
        store=True,
        readonly=True,
        compute="_compute_kpi_result",
    )

    def action_compute_realization(self):
        """Recompute realization, score, final score, and result.

        Runs the full recomputation chain on ``line_ids`` (as
        superuser) followed by ``_compute_kpi_result``.
        """
        for record in self.sudo():
            record.line_ids._compute_realization()
            record.line_ids._compute_score()
            record.line_ids._compute_final_score()
            record._compute_kpi_result()

    def action_populate_kpi(self):
        """Rebuild ``line_ids``/``user_ids`` from ``kpi_template_id``.

        Discards existing lines (and their score ranges) and
        recreates them from the template's lines, then refreshes the
        appraiser list via ``_get_user_ids`` and copies the template's
        score category.
        """
        for record in self.sudo():
            result = []
            if record.kpi_template_id:
                record.line_ids.score_range_ids.unlink()
                record.line_ids.unlink()
                record.user_ids = False

                for line in record.kpi_template_id.line_ids:
                    value = {
                        "kpi_item_id": line.kpi_item_id.id,
                        "weight": line.weight,
                        "target": line.target,
                        "realization_method": line.realization_method,
                        "use_realization_limit": line.use_realization_limit,
                        "min_realization_limit": line.min_realization_limit,
                        "max_realization_limit": line.max_realization_limit,
                        "score_method": line.score_method,
                        "use_score_limit": line.use_score_limit,
                        "min_score_limit": line.min_score_limit,
                        "max_score_limit": line.max_score_limit,
                        "python_code": line.python_code,
                    }
                    if line.score_method == "range":
                        if line.score_range_ids:
                            list_range = []
                            for range in line.score_range_ids:
                                value_range = {
                                    "min_value": range.min_value,
                                    "max_value": range.max_value,
                                    "score": range.score,
                                }
                                list_range.append((0, 0, value_range))
                            value["score_range_ids"] = list_range
                    result.append((0, 0, value))
                record.line_ids = result
                record.user_ids = record._get_user_ids()
                record.kpi_score_categ_id = record.kpi_template_id.kpi_score_categ_id

    def _get_user_ids(self):
        """Resolve the appraisers per ``kpi_template_id`` selection.

        Reads ``appraisal_selection_method`` on the template: fixed
        users, group members, both, or a Python code evaluation that
        must set a ``user`` list in its localdict.

        :return: list of unique ``res.users`` ids
        :raises UserError: if the Python code path does not set
            ``user`` in its result
        """
        self.ensure_one()
        list_user = []
        appraisal_selection_method = self.kpi_template_id.appraisal_selection_method

        if appraisal_selection_method == "use_user":
            user_ids = self.kpi_template_id.user_ids
            if user_ids:
                list_user += user_ids.ids
        elif appraisal_selection_method == "use_group":
            group_ids = self.kpi_template_id.group_ids
            if group_ids:
                for group in group_ids:
                    list_user += group.users.ids
        elif appraisal_selection_method == "use_both":
            user_ids = self.kpi_template_id.user_ids
            if user_ids:
                list_user += user_ids.ids
            group_ids = self.kpi_template_id.group_ids
            if group_ids:
                for group in group_ids:
                    list_user += group.users.ids
        else:
            python_code = self.kpi_template_id.python_code
            result = self._evaluate_python_code(python_code)
            if result:
                if "user" in result:
                    list_user += result["user"]
                else:
                    msg_err = "No User defines on python code"
                    raise UserError(_(msg_err))
        return list(set(list_user))

    def _get_localdict(self):
        """Build the ``safe_eval`` context for the template's code.

        :return: dict exposing ``document`` (this record) and ``env``
        """
        return {
            "document": self,
            "env": self.env,
        }

    def _evaluate_python_code(self, python_condition):
        """Evaluate ``python_condition`` and return its localdict.

        :param python_condition: Python source expected to set
            ``user`` in its execution scope
        :return: the localdict after execution
        :raises UserError: if evaluation raises any exception
        """
        localdict = self._get_localdict()
        result = False
        try:
            safe_eval(
                python_condition, globals_dict=localdict, mode="exec", nocopy=True
            )
            result = localdict
        except Exception:
            msg_err = "Error when execute python code"
            raise UserError(_(msg_err))

        return result

    def _prepare_kpi_appraisal_data(self, user):
        """Build the ``mixin.kpi_appraisal`` values for ``user``.

        :param user: ``res.users`` record the appraisal is created for
        :return: dict of values for ``mixin.kpi_appraisal.create``
        """
        self.ensure_one()
        data = {
            "kpi_id": self.id,
            "user_id": user.id,
        }
        return data

    def _prepare_kpi_appraisal_line_data(self, appraisal_id, kpi_line):
        """Build the ``mixin.kpi_appraisal_line`` values for a line.

        :param appraisal_id: ``mixin.kpi_appraisal`` record owning
            the new line
        :param kpi_line: ``mixin.kpi_line`` the appraisal line rates
        :return: dict of values for
            ``mixin.kpi_appraisal_line.create``
        """
        self.ensure_one()
        data = {
            "kpi_appraisal_id": appraisal_id.id,
            "kpi_line_id": kpi_line.id,
        }
        return data

    @ssi_decorator.post_approve_action()
    def _create_kpi_appraisals(self):
        """Create one appraisal per user, with a line per KPI item.

        Runs after approval. Skips lines whose
        ``realization_method`` is ``python`` since those do not
        require a human appraiser.
        """
        self.ensure_one()
        obj_kpi_appraisal = self.env[self.appraisal_ids._name]
        obj_kpi_appraisal_line = self.env[self.appraisal_ids.line_ids._name]
        for user in self.user_ids:
            appraisal_id = obj_kpi_appraisal.create(
                self._prepare_kpi_appraisal_data(user)
            )
            for kpi_line in self.line_ids.filtered(
                lambda x: x.realization_method != "python"
            ):
                obj_kpi_appraisal_line.create(
                    self._prepare_kpi_appraisal_line_data(appraisal_id, kpi_line)
                )

    @ssi_decorator.pre_cancel_action()
    def _10_remove_appraisal_ids(self):
        """Remove appraisals before cancelling, blocking if any is done.

        :raises UserError: if any linked appraisal already has state
            ``done``
        """
        self.ensure_one()
        check_appraisal = self.appraisal_ids.filtered(lambda x: x.state == "done")
        if check_appraisal:
            strWarning = _("One or more user appraisal has been done")
            raise UserError(strWarning)
        else:
            ctx = {"force_unlink": True}
            self.with_context(ctx).appraisal_ids.unlink()

    @ssi_decorator.pre_done_check()
    def _10_check_appraisal_state(self):
        """Block ``done`` until every appraisal is completed.

        :raises UserError: if any linked appraisal is not ``done``
        """
        self.ensure_one()
        check = self.appraisal_ids.filtered(lambda x: x.state != "done")
        if check:
            strWarning = _("All appraisals must be done")
            raise UserError(strWarning)

    @ssi_decorator.post_done_action()
    def _10_recompute_realization(self):
        """Recompute realization/score once the document is done."""
        self.ensure_one()
        self.action_compute_realization()

    @ssi_decorator.pre_confirm_check()
    def _01_check_amount_weight(self):
        """Block confirm unless total line weight is exactly 100%.

        :raises UserError: if ``amount_weight`` is not ``100.0``
        """
        self.ensure_one()
        strWarning = _("Total weight must be 100.0%")
        if self.amount_weight != 100.0:
            raise UserError(strWarning)

    @api.constrains(
        "date_start",
        "date_end",
    )
    def _constrains_overlap(self):
        """Forbid overlapping KPI periods for the same subject.

        Delegates the overlap test to ``_check_overlap``, implemented
        per concrete model (employee/department).

        :raises UserError: if ``_check_overlap`` reports an overlap
        """
        for record in self.sudo():
            if not record._check_overlap():
                error_message = _(
                    """
                Context: Constrains
                Database ID: %s
                Problem: There are other KPI that overlap
                Solution: Change date start and date end
                """
                    % (record.id)
                )
                raise UserError(error_message)
