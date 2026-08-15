# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiItem(models.Model):
    """
    Master data for a KPI item (e.g. "Sales Growth", "On-Time
    Delivery"). Referenced by KPI template lines and KPI lines to
    identify what is being measured.
    """

    _name = "kpi_item"
    _inherit = ["mixin.master_data"]
    _description = "KPI Item"

    name = fields.Char(
        string="Item",
    )
    code = fields.Char(
        default="/",
    )
