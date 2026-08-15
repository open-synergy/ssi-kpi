# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass (see odoo-development-ui-test skill).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiKpiEmployee(HttpSavepointCase):
    """Tour tests for the ``kpi.employee`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Build the template, employees, and records the tours need.

        One dedicated ``hr.employee`` is created per tour so the
        ``_check_overlap`` constraint (same employee, overlapping
        period) never triggers between fixtures that share the same
        date range. Records are created/transitioned with
        ``with_user(cls.admin)`` so policy/approval checks evaluate
        against the same identity the tour logs in as.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Config (IK Pre-Condition "Data"): one KPI item + one KPI
        # template whose single line is worth 100% of the weight, so
        # Confirm's total-weight check (`_01_check_amount_weight`)
        # passes without further setup.
        cls.kpi_item = cls.env["kpi_item"].create(
            {"name": "TOUR KPI Item", "code": "TOUR-KPI-ITEM-EMP"}
        )
        cls.kpi_template = cls.env["kpi_template"].create(
            {
                "name": "TOUR KPI Employee Template",
                "code": "TOUR-KPI-EMP-TPL",
                "type": "employee",
                "appraisal_selection_method": "use_user",
                "user_ids": [(6, 0, [cls.admin.id])],
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "kpi_item_id": cls.kpi_item.id,
                            "weight": 100.0,
                            "target": 100.0,
                            "realization_method": "python",
                        },
                    )
                ],
            }
        )

        # Global wizard reasons for the Cancel (10-cancel) and
        # Terminate (11-terminate) tours.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {"name": "TOUR Cancel Reason", "code": "TOUR-CANCEL", "global_use": True}
        )
        cls.terminate_reason = cls.env["base.terminate_reason"].create(
            {
                "name": "TOUR Terminate Reason",
                "code": "TOUR-TERMINATE",
                "global_use": True,
            }
        )

        Employee = cls.env["hr.employee"]
        cls.employee_create = Employee.create({"name": "TOUR KPI EMP Create"})
        cls.employee_edit = Employee.create({"name": "TOUR KPI EMP Edit"})
        cls.employee_delete = Employee.create({"name": "TOUR KPI EMP Delete"})
        cls.employee_confirm = Employee.create({"name": "TOUR KPI EMP Confirm"})
        cls.employee_approve = Employee.create({"name": "TOUR KPI EMP Approve"})
        cls.employee_reject = Employee.create({"name": "TOUR KPI EMP Reject"})
        cls.employee_finish = Employee.create({"name": "TOUR KPI EMP Finish"})
        cls.employee_cancel = Employee.create({"name": "TOUR KPI EMP Cancel"})
        cls.employee_terminate = Employee.create({"name": "TOUR KPI EMP Terminate"})
        cls.employee_restart = Employee.create({"name": "TOUR KPI EMP Restart"})
        cls.employee_compute = Employee.create({"name": "TOUR KPI EMP Compute"})

        kpi_employee_model = cls.env["kpi.employee"].with_user(cls.admin)

        def make_kpi_employee(employee):
            """Create a fully-populated draft ``kpi.employee`` record.

            :param employee: ``hr.employee`` the record is for
            :return: the created, unsaved-in-UI-sense ``kpi.employee``
                record (already committed via ORM `create`)
            """
            return kpi_employee_model.create(
                {
                    "employee_id": employee.id,
                    "user_id": cls.admin.id,
                    "date_start": "2030-01-01",
                    "date_end": "2030-01-31",
                    "kpi_template_id": cls.kpi_template.id,
                    "user_ids": [(6, 0, [cls.admin.id])],
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "kpi_item_id": cls.kpi_item.id,
                                "weight": 100.0,
                                "target": 100.0,
                                "realization_method": "python",
                            },
                        )
                    ],
                }
            )

        # IK: docs/kpi_employee/02-edit.md -- Draft, already populated
        # once; the tour only needs to run Populate again.
        cls.kpi_edit = make_kpi_employee(cls.employee_edit)

        # IK: docs/kpi_employee/03-delete.md -- Draft, "/" number.
        cls.kpi_delete = make_kpi_employee(cls.employee_delete)

        # IK: docs/kpi_employee/04-confirm.md -- Draft, weight at 100%.
        cls.kpi_confirm = make_kpi_employee(cls.employee_confirm)

        # IK: docs/kpi_employee/05-approve.md and 06-reject.md --
        # Pre-Condition is Waiting for Approval, reached here in
        # Python (Confirm itself is a different tour's Flow).
        cls.kpi_approve = make_kpi_employee(cls.employee_approve)
        cls.kpi_approve.action_confirm()
        cls.kpi_reject = make_kpi_employee(cls.employee_reject)
        cls.kpi_reject.action_confirm()

        # IK: docs/kpi_employee/09-finish.md, 11-terminate.md,
        # 14-compute-realization.md -- Pre-Condition is In Progress,
        # reached by Confirm + Approve (single approval level; admin
        # is a member of the configured approver group).
        cls.kpi_finish = make_kpi_employee(cls.employee_finish)
        cls.kpi_finish.action_confirm()
        cls.kpi_finish.action_approve_approval()
        # 09-finish Pre-Condition: every appraisal is Done. The
        # appraisal model has no IK/tour of its own (out of scope for
        # this item) -- its state is set directly here as
        # Pre-Condition setup, not as the flow under test.
        cls.kpi_finish.appraisal_ids.sudo().write({"state": "done"})

        cls.kpi_terminate = make_kpi_employee(cls.employee_terminate)
        cls.kpi_terminate.action_confirm()
        cls.kpi_terminate.action_approve_approval()

        cls.kpi_compute = make_kpi_employee(cls.employee_compute)
        cls.kpi_compute.action_confirm()
        cls.kpi_compute.action_approve_approval()

        # IK: docs/kpi_employee/10-cancel.md -- Draft is one of the
        # cancellable states; no appraisal exists yet.
        cls.kpi_cancel = make_kpi_employee(cls.employee_cancel)

        # IK: docs/kpi_employee/12-restart.md -- Pre-Condition is
        # Cancelled, reached via the real `action_cancel` so the
        # fixture matches what 10-cancel actually produces.
        cls.kpi_restart = make_kpi_employee(cls.employee_restart)
        cls.kpi_restart.action_cancel(cls.cancel_reason)

    def test_create(self):
        """Run the create tour for ``kpi.employee``.

        IK: docs/kpi_employee/01-create.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``kpi.employee``.

        IK: docs/kpi_employee/02-edit.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``kpi.employee``.

        IK: docs/kpi_employee/03-delete.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``kpi.employee``.

        IK: docs/kpi_employee/04-confirm.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``kpi.employee``.

        IK: docs/kpi_employee/05-approve.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``kpi.employee``.

        IK: docs/kpi_employee/06-reject.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_reject", login="admin")

    def test_finish(self):
        """Run the finish tour for ``kpi.employee``.

        IK: docs/kpi_employee/09-finish.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_finish", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``kpi.employee``.

        IK: docs/kpi_employee/10-cancel.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_cancel", login="admin")

    def test_terminate(self):
        """Run the terminate tour for ``kpi.employee``.

        IK: docs/kpi_employee/11-terminate.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_terminate", login="admin")

    def test_restart(self):
        """Run the restart tour for ``kpi.employee``.

        IK: docs/kpi_employee/12-restart.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_employee_restart", login="admin")

    def test_compute_realization(self):
        """Run the Compute tour for ``kpi.employee``.

        IK: docs/kpi_employee/14-compute-realization.md
        """
        self.start_tour(
            "/web", "ssi_kpi_kpi_employee_compute_realization", login="admin"
        )
