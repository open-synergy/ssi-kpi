# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass (see odoo-development-ui-test skill).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiKpiDepartment(HttpSavepointCase):
    """Tour tests for the ``kpi.department`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Build the template, departments, and records the tours need.

        One dedicated ``hr.department`` is created per tour so the
        ``_check_overlap`` constraint (same department, overlapping
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
            {"name": "TOUR KPI Item", "code": "TOUR-KPI-ITEM-DEPT"}
        )
        cls.kpi_template = cls.env["kpi_template"].create(
            {
                "name": "TOUR KPI Department Template",
                "code": "TOUR-KPI-DEPT-TPL",
                "type": "department",
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
            {"name": "TOUR Cancel Reason", "code": "TOUR-CANCEL-D", "global_use": True}
        )
        cls.terminate_reason = cls.env["base.terminate_reason"].create(
            {
                "name": "TOUR Terminate Reason",
                "code": "TOUR-TERMINATE-D",
                "global_use": True,
            }
        )

        Department = cls.env["hr.department"]
        cls.department_create = Department.create({"name": "TOUR KPI DEPT Create"})
        cls.department_edit = Department.create({"name": "TOUR KPI DEPT Edit"})
        cls.department_delete = Department.create({"name": "TOUR KPI DEPT Delete"})
        cls.department_confirm = Department.create({"name": "TOUR KPI DEPT Confirm"})
        cls.department_approve = Department.create({"name": "TOUR KPI DEPT Approve"})
        cls.department_reject = Department.create({"name": "TOUR KPI DEPT Reject"})
        cls.department_finish = Department.create({"name": "TOUR KPI DEPT Finish"})
        cls.department_cancel = Department.create({"name": "TOUR KPI DEPT Cancel"})
        cls.department_terminate = Department.create(
            {"name": "TOUR KPI DEPT Terminate"}
        )
        cls.department_restart = Department.create({"name": "TOUR KPI DEPT Restart"})
        cls.department_compute = Department.create({"name": "TOUR KPI DEPT Compute"})

        kpi_department_model = cls.env["kpi.department"].with_user(cls.admin)

        def make_kpi_department(department):
            """Create a fully-populated draft ``kpi.department`` record.

            :param department: ``hr.department`` the record is for
            :return: the created ``kpi.department`` record
            """
            return kpi_department_model.create(
                {
                    "department_id": department.id,
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

        # IK: docs/kpi_department/02-edit.md -- Draft, already
        # populated once; the tour only needs to run Populate again.
        cls.kpi_edit = make_kpi_department(cls.department_edit)

        # IK: docs/kpi_department/03-delete.md -- Draft, "/" number.
        cls.kpi_delete = make_kpi_department(cls.department_delete)

        # IK: docs/kpi_department/04-confirm.md -- Draft, weight 100%.
        cls.kpi_confirm = make_kpi_department(cls.department_confirm)

        # IK: docs/kpi_department/05-approve.md and 06-reject.md --
        # Pre-Condition is Waiting for Approval, reached here in
        # Python (Confirm itself is a different tour's Flow).
        cls.kpi_approve = make_kpi_department(cls.department_approve)
        cls.kpi_approve.action_confirm()
        cls.kpi_reject = make_kpi_department(cls.department_reject)
        cls.kpi_reject.action_confirm()

        # IK: docs/kpi_department/09-finish.md, 11-terminate.md,
        # 14-compute-realization.md -- Pre-Condition is In Progress,
        # reached by Confirm + Approve (single approval level; admin
        # is a member of the configured approver group).
        cls.kpi_finish = make_kpi_department(cls.department_finish)
        cls.kpi_finish.action_confirm()
        cls.kpi_finish.action_approve_approval()
        # 09-finish Pre-Condition: every appraisal is Done. The
        # appraisal model has no IK/tour of its own (out of scope for
        # this item) -- its state is set directly here as
        # Pre-Condition setup, not as the flow under test.
        cls.kpi_finish.appraisal_ids.sudo().write({"state": "done"})

        cls.kpi_terminate = make_kpi_department(cls.department_terminate)
        cls.kpi_terminate.action_confirm()
        cls.kpi_terminate.action_approve_approval()

        cls.kpi_compute = make_kpi_department(cls.department_compute)
        cls.kpi_compute.action_confirm()
        cls.kpi_compute.action_approve_approval()

        # IK: docs/kpi_department/10-cancel.md -- Draft is one of the
        # cancellable states; no appraisal exists yet.
        cls.kpi_cancel = make_kpi_department(cls.department_cancel)

        # IK: docs/kpi_department/12-restart.md -- Pre-Condition is
        # Cancelled, reached via the real `action_cancel` so the
        # fixture matches what 10-cancel actually produces.
        cls.kpi_restart = make_kpi_department(cls.department_restart)
        cls.kpi_restart.action_cancel(cls.cancel_reason)

    def test_create(self):
        """Run the create tour for ``kpi.department``.

        IK: docs/kpi_department/01-create.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``kpi.department``.

        IK: docs/kpi_department/02-edit.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``kpi.department``.

        IK: docs/kpi_department/03-delete.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``kpi.department``.

        IK: docs/kpi_department/04-confirm.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``kpi.department``.

        IK: docs/kpi_department/05-approve.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``kpi.department``.

        IK: docs/kpi_department/06-reject.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_reject", login="admin")

    def test_finish(self):
        """Run the finish tour for ``kpi.department``.

        IK: docs/kpi_department/09-finish.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_finish", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``kpi.department``.

        IK: docs/kpi_department/10-cancel.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_cancel", login="admin")

    def test_terminate(self):
        """Run the terminate tour for ``kpi.department``.

        IK: docs/kpi_department/11-terminate.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_terminate", login="admin")

    def test_restart(self):
        """Run the restart tour for ``kpi.department``.

        IK: docs/kpi_department/12-restart.md
        """
        self.start_tour("/web", "ssi_kpi_kpi_department_restart", login="admin")

    def test_compute_realization(self):
        """Run the Compute tour for ``kpi.department``.

        IK: docs/kpi_department/14-compute-realization.md
        """
        self.start_tour(
            "/web", "ssi_kpi_kpi_department_compute_realization", login="admin"
        )
