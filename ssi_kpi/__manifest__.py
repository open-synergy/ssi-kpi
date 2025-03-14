# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=C8101
{
    "name": "HR - Key Perfomance Indicator (KPI)",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_hr",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_transaction_terminate_mixin",
        "ssi_duration_mixin",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/kpi_employee_ir_rule_data.xml",
        "security/kpi_department_ir_rule_data.xml",
        "menu.xml",
        "data/approval_employee_template_data.xml",
        "data/approval_department_template_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_kpi_employee_template_data.xml",
        "data/sequence_kpi_department_template_data.xml",
        "data/policy_kpi_employee_template_data.xml",
        "data/policy_kpi_employee_appraisal_template_data.xml",
        "data/policy_kpi_department_template_data.xml",
        "data/policy_kpi_department_appraisal_template_data.xml",
        "views/kpi_item_views.xml",
        "views/kpi_template_views.xml",
        "views/kpi_template_line_views.xml",
        "views/kpi_employee_views.xml",
        "views/kpi_employee_line_views.xml",
        "views/kpi_employee_appraisal_views.xml",
        "views/kpi_employee_appraisal_line_views.xml",
        "views/kpi_department_views.xml",
        "views/kpi_department_line_views.xml",
        "views/kpi_department_appraisal_views.xml",
        "views/kpi_department_appraisal_line_views.xml",
        "views/kpi_score_categ_views.xml",
        "views/kpi_score_categ_range_value_views.xml",
    ],
}
