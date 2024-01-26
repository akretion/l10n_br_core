# Copyright (C) 2013  Renato Lima - Akretion
# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    certificate_ecnpj_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.certificate",
        string="E-CNPJ",
        domain="[('type', '=', 'e-cnpj')]",
    )

    certificate_nfe_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.certificate",
        string="NFe",
        domain="[('type', '=', 'nf-e')]",
    )

    certificate = fields.Many2one(
        comodel_name="l10n_br_fiscal.certificate",
        compute="_compute_certificate",
    )

    def _compute_certificate(self):
        for record in self:
            certificate = False
            if record.sudo().certificate_nfe_id:
                certificate = record.sudo().certificate_nfe_id
            elif record.sudo().certificate_ecnpj_id:
                certificate = record.sudo().certificate_ecnpj_id

            if not certificate:
                raise ValidationError(
                    _(
                        "Certificate not found, you need to inform your e-CNPJ"
                        " or e-NFe certificate in the Company."
                    )
                )

            record.certificate = certificate
