# Copyright 2019 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WizardDocumentInvalidate(models.TransientModel):

    _name = "l10n_br_fiscal.wizard_document_invalidate"
    _description = "Document fiscal cancel wizard"

    initial_number = fields.Integer(
        string='Número inicial',
    )

    final_number = fields.Integer(
        string='Número final'
    )

    justificative = fields.Text("Justificativa", size=255, required=True)

    @api.constrains("justificative")
    @api.multi
    def _check_justificative(self):
        for record in self:
            if len(record.justificative) < 15:
                raise UserError(
                    _("Justificativa deve ter o tamanho mínimo de 15 " "caracteres.")
                )

    @api.multi
    def doit(self):
        for wizard in self:
            obj = self.env[self.env.context["active_model"]].browse(
                self.env.context["active_id"]
            )
            obj.invalidate(wizard.initial_number, wizard.final_number,
                           wizard.justificative)
        return {"type": "ir.actions.act_window_close"}
