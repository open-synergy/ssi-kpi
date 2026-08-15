# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestKpi(YamlTransactionCase):
    """Cover ``kpi.employee``/``kpi.department`` compute and checks."""

    def test_kpi(self):
        """Run the KPI create/compute/negative-path YAML scenarios."""
        self.run_yaml_scenario("test_data_kpi.yaml")
