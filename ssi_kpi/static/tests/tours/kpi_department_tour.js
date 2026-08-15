/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_kpi.kpi_department_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared Flow 1 — Open the Human Resource > KPI > Departments menu.
    // "KPI Departments" is not a substring of the app's landing action
    // title ("Employees"), so the breadcrumb gate below cannot match
    // the stale landing view.
    function openMenuSteps() {
        return [
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
        ];
    }

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/01-create.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_create",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Click the New button
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

            // Flow 3 — Fill in the required fields
            {
                content: "Select the Department",
                trigger: ".o_field_many2one[name='department_id'] input",
                run: "text TOUR KPI DEPT Create",
            },
            {
                content: "Pick the Department",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR KPI DEPT Create)",
                in_modal: false,
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                run: "text 01/01/2030",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                run: "text 01/31/2030",
            },
            {
                content: "Select the Template",
                trigger: ".o_field_many2one[name='kpi_template_id'] input",
                run: "text TOUR KPI Department Template",
            },
            {
                content: "Pick the Template",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR KPI Department Template)",
                in_modal: false,
            },

            // Flow 4 — Click Populate on the Details tab
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },
            {
                content: "Click Populate",
                trigger: "button[name='action_populate_kpi']",
            },
            {
                // Gate: this row cannot exist before Populate is
                // clicked — line_ids starts empty on a new record.
                content: "Details line is populated from the Template",
                trigger:
                    ".o_field_x2many[name='line_ids'] .o_data_row:contains(TOUR KPI Item)",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 5 — Click Save
            {content: "Save the record", trigger: ".o_form_button_save"},
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },

            // Post-Condition — A new record is created in Draft status
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/02-edit.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_edit",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Find and open the record to edit
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR KPI DEPT Edit) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Edit button (14.0)
            {content: "Click the Edit button", trigger: ".o_form_button_edit"},
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 4 — Change the required fields
            {
                content: "Change Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                run: "text 02/15/2030",
            },

            // Flow 5 — Click Populate on the Details tab
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },
            {
                content: "Click Populate",
                trigger: "button[name='action_populate_kpi']",
            },
            {
                // Gate: the Details line already exists before this
                // click (fixture is pre-populated), so a bare
                // data-row gate would be false-positive, and so is
                // `button[...]:enabled` -- CI evidence showed it
                // resolving before Populate's write+reload cycle
                // landed, letting the next Save step race a still
                // in-flight reload (odoo-development-ui-test skill
                // Sec. P). The fixture line's weight/target (40.0)
                // deliberately differ from the Template's (100.0), so
                // this gate can wait on the row switching to the
                // Template's value -- impossible to match before
                // Populate actually replaces the line.
                content: "Populate has finished",
                trigger:
                    ".o_field_x2many[name='line_ids'] .o_data_row:contains(TOUR KPI Item) .o_list_number:contains(100.00)",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 6 — Click Save
            {content: "Save the record", trigger: ".o_form_button_save"},

            // Post-Condition — The record is updated with the new values
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/03-delete.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_delete",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to delete
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Delete) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click Action > Delete
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                // The Action menu item is an Owl component; match the
                // label exactly so "Delete" is not confused with
                // another item such as "Duplicate".
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },

            // Flow 4 — Click OK on the confirmation dialog
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Back to the KPI Departments list",
                trigger: ".breadcrumb-item.o_back_button a:contains(KPI Departments)",
            },

            // Post-Condition — The record is permanently removed
            {
                content: "Record no longer appears in the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR KPI DEPT Delete)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/04-confirm.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_confirm",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to confirm
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Confirm) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Confirm button
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Waiting for Approval
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/05-approve.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_approve",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to approve
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Approve) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Approve button
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — All levels fulfilled: auto-moves to
            // In Progress via `_after_approved_method` (action_open).
            {
                content: "Status is In Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/06-reject.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_reject",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to reject
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Reject) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Reject button
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Reject
            {
                content: "Status is Reject",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/09-finish.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_finish",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to finish
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Finish) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Done button
            {
                content: "Click the Done button",
                trigger: ".o_statusbar_buttons button[name='action_done']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Done
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/10-cancel.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_cancel",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to cancel
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Cancel) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Cancel button
            // `type="action"` button: `name` is a numeric action id at
            // render time, so it must be targeted by its label.
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains(Cancel)",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Select the Cancellation Reason in the wizard
            {
                content: "Wizard is open",
                // 14.0: do not prefix with `.modal` — the trigger is
                // already searched inside the modal.
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                // `cancel_reason_id` uses `widget="radio"` (see
                // base_select_cancel_reason_views.xml) — a set of
                // radio buttons, not a many2one autocomplete input.
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item label:contains(TOUR Cancel Reason)",
            },

            // Flow 5 — Click Confirm
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Cancelled
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/11-terminate.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_terminate",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to terminate
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Terminate) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Terminate button
            // `type="action"` button: `name` is a numeric action id at
            // render time, so it must be targeted by its label.
            {
                content: "Click the Terminate button",
                trigger: ".o_statusbar_buttons button:enabled:contains(Terminate)",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Select the Termination Reason in the wizard
            {
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                // `terminate_reason_id` uses `widget="radio"` (see
                // base_select_terminate_reason_views.xml) — a set of
                // radio buttons, not a many2one autocomplete input.
                content: "Select the termination reason",
                trigger:
                    ".o_field_widget[name='terminate_reason_id'] .o_radio_item label:contains(TOUR Terminate Reason)",
            },

            // Flow 5 — Click Confirm
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status changes to Terminate
            {
                content: "Status is Terminate",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='terminate'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/12-restart.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_restart",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to restart
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Restart) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Restart button
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — Status returns to Draft
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // ─────────────────────────────────────────────────────────────
    // IK: docs/kpi_department/14-compute-realization.md
    // ─────────────────────────────────────────────────────────────
    tour.register(
        "ssi_kpi_kpi_department_compute_realization",
        {test: true, url: "/web"},
        [].concat(openMenuSteps(), [
            // Flow 2 — Open the record to recompute
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR KPI DEPT Compute) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — On the Details tab, click the Compute button
            {
                content: "Open the Details tab",
                trigger: ".o_notebook .nav-link:contains(Details)",
            },
            {
                content: "Click the Compute button",
                trigger: "button[name='action_compute_realization']",
            },
            {
                // Gate: Compute does not add/remove rows, so the only
                // signal is the button's own state. Odoo 14 disables
                // a `type="object"` button synchronously on click and
                // re-enables it only after the write cycle completes.
                content: "Compute has finished",
                trigger: "button[name='action_compute_realization']:enabled",
                run: function () {
                    // Assertion only.
                },
            },

            // Post-Condition — Status remains In Progress
            {
                content: "Status is still In Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );
});
