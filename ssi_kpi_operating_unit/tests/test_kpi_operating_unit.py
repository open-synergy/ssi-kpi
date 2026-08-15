# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestKpiOperatingUnit(YamlTransactionCase):
    """Cover operating unit scoping on the KPI models.

    Covers ``kpi.employee``, ``kpi.department``, and their
    appraisal counterparts, checking that ``operating_unit_id`` can
    be set on creation.
    """

    def test_kpi_operating_unit(self):
        """Run the operating unit scenarios for the KPI models."""
        self.run_yaml_scenario("test_data_kpi_operating_unit.yaml")
