# Copyright 2023 - TODAY, Akretion - Raphael Valyi <raphael.valyi@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/sped-extractor and xsdata-odoo

from odoo import fields, models


class SpecMixinEFDPISCOFINS(models.AbstractModel):
    _name = "l10n_br_sped.mixin.efd_pis_cofins"
    _description = "l10n_br_sped.mixin.efd_pis_cofins"
    _inherit = "l10n_br_sped.mixin"

    declaration_id = fields.Many2one(
        comodel_name="l10n_br_sped.efd_pis_cofins.0000",
        required=True,
    )
