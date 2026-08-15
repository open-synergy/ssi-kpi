# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass (see odoo-development-ui-test skill).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiKpiEmployeeOperatingUnit(HttpSavepointCase):
    """Tour tests for the ``kpi.employee`` Operating Unit delta."""

    @classmethod
    def setUpClass(cls):
        """Grant admin the multi operating unit group.

        The ``operating_unit_id`` field is gated by
        ``operating_unit.group_multi_operating_unit`` in the view; the
        tour logs in as ``admin``, so the group must be granted here
        or the field never renders (see odoo-development-ui-test
        skill, "Additional Fields" delta tours pattern).
        """
        super().setUpClass()
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

    def test_create(self):
        """Run the create delta tour for ``kpi.employee``.

        IK: docs/kpi_employee/01-create.md
        """
        self.start_tour(
            "/web", "ssi_kpi_operating_unit_kpi_employee_create", login="admin"
        )
