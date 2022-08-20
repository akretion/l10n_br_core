# Copyright 2022 Engenere
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models


class FieldSelectWizard(models.TransientModel):

    _name = "field.select.wizard"
    _description = "Field Select Wizard"

    content_source_field = fields.Char()

    content_source_field_view = fields.Char(
        compute="_compute_content_source_field_view",
    )

    cnab_field_id = fields.Many2one(
        comodel_name="l10n_br_cnab.line.field",
        string="CNAB Field",
    )

    content_source_model_id = fields.Many2one(
        "ir.model",
        string="Related Model",
        related="cnab_field_id.content_source_model_id",
    )

    new_field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        domain="[('model_id', '=', parent_model_id)]",
    )

    parent_model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Parent Model",
        compute="_compute_parent_model_id",
    )

    @api.depends("content_source_model_id")
    def _compute_parent_model_id(self):
        model = self.content_source_model_id
        if self.content_source_field:
            dn_fields = self.content_source_field.split(".")
            for fld in dn_fields:
                field_id = self.env["ir.model.fields"].search(
                    [("model_id", "=", model.id), ("name", "=", fld)]
                )
                model = self.env["ir.model"].search([("model", "=", field_id.relation)])
        self.parent_model_id = model

    def _update_dot_notation(self):
        if self.new_field_id:
            self.content_source_field = self.content_source_field or ""
            self.content_source_field += "." if self.content_source_field else ""
            self.content_source_field += self.new_field_id.name

    def action_confirm(self):
        "Action Confirm"
        self.cnab_field_id.content_source_field = self.content_source_field
        return

    def action_remove_last_field(self):
        "Action Confirm"
        strings = self.content_source_field.split(".")[:-1]
        self.content_source_field = ".".join(strings)
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "res_model": "field.select.wizard",
            "target": "new",
            "context": {
                "default_cnab_field_id": self.cnab_field_id.id,
                "default_content_source_field": self.content_source_field,
            },
        }

    def _compute_content_source_field_view(self):
        self.content_source_field_view = self.content_source_field.replace(".", "→")

    def action_add_field(self):
        "Action Add Field"
        self._update_dot_notation()
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "res_model": "field.select.wizard",
            "target": "new",
            "context": {
                "default_cnab_field_id": self.cnab_field_id.id,
                "default_content_source_field": self.content_source_field,
            },
        }
