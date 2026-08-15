/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_kpi_operating_unit.kpi_department_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/01-create.md (delta — Additional
    // Fields). Extends ssi_kpi docs/kpi_department/01-create.md
    // Flow 1-2.
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_operating_unit_kpi_department_create",
        {test: true, url: "/web"},
        [
            // Flow 1 (base) — Open the Human Resource > KPI >
            // Departments menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the KPI menu",
                trigger: '.o_menu_sections [data-menu-xmlid="ssi_kpi.kpi_root_menu"]',
            },
            {
                content: "Open the Departments menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_kpi.kpi_department_menu"]',
            },
            {
                content: "KPI Departments list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(KPI Departments)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 2 (base) — Click the New button.
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },

            // Delta — Additional Fields: Operating Unit is displayed.
            {
                content: "Operating Unit field is displayed",
                trigger: ".o_field_widget[name='operating_unit_id']",
                run: function () {
                    // Assertion only. Stop here -- this is a delta
                    // tour (odoo-development-ui-test skill, arketipe
                    // E1); it does not continue into the base
                    // create/confirm/approve flow.
                },
            },
        ]
    );
});
