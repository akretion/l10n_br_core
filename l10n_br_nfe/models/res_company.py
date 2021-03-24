# Copyright 2019 Akretion (Raphaël Valyi <raphael.valyi@akretion.com>)
# Copyright 2019 KMEE INFORMATICA LTDA
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields

from odoo.addons.spec_driven_model.models import spec_models

from ..constants.nfe import (
    NFE_ENVIRONMENT_DEFAULT,
    NFE_ENVIRONMENTS,
    NFE_VERSION_DEFAULT,
    NFE_VERSIONS,
)

PROCESSADOR_ERPBRASIL_EDOC = 'oca'
PROCESSADOR = [(PROCESSADOR_ERPBRASIL_EDOC, 'erpbrasil.edoc')]


class ResCompany(spec_models.SpecModel):
    _name = 'res.company'
    _inherit = ['res.company', 'nfe.40.emit']
    _nfe_search_keys = ['nfe40_CNPJ', 'nfe40_xNome', 'nfe40_xFant']

    def _compute_nfe_data(self):
        # compute because a simple related field makes the match_record fail
        for rec in self:
            if rec.partner_id.is_company:
                rec.nfe40_choice6 = 'nfe40_CNPJ'
                rec.nfe40_CNPJ = rec.partner_id.cnpj_cpf
            else:
                rec.nfe40_choice6 = 'nfe40_CPF'
                rec.nfe40_CPF = rec.partner_id.cnpj_cpf

    nfe40_CNPJ = fields.Char(compute='_compute_nfe_data')
    nfe40_xNome = fields.Char(related='partner_id.legal_name')
    nfe40_xFant = fields.Char(related='partner_id.name')
    nfe40_IE = fields.Char(related='partner_id.inscr_est')
    nfe40_CRT = fields.Selection(related='tax_framework')
    nfe40_enderEmit = fields.Many2one('res.partner', related='partner_id')

    nfe40_choice6 = fields.Selection(
        compute='_compute_nfe_data'
    )

    processador_edoc = fields.Selection(
        selection_add=PROCESSADOR,
    )

    nfe_version = fields.Selection(
        selection=NFE_VERSIONS,
        string='NFe Version',
        default=NFE_VERSION_DEFAULT,
    )

    nfe_environment = fields.Selection(
        selection=NFE_ENVIRONMENTS,
        string='NFe Environment',
        default=NFE_ENVIRONMENT_DEFAULT,
    )

    nfe_default_serie_id = fields.Many2one(
        comodel_name='l10n_br_fiscal.document.serie',
        string='NF-e Default Serie',
    )

    def _build_attr(self, node, fields, vals, path, attr):
        if attr.get_name() == 'enderEmit'\
                and self.env.context.get('edoc_type') == 'in':
            # we don't want to try build a related partner_id for enderEmit
            # when importing an NFe
            # instead later the emit tag will be imported as the
            # document partner_id (dest) and the enderEmit data will be
            # injected in the same res.partner record.
            return
        return super()._build_attr(node, fields, vals, path, attr)

    @api.model
    def _prepare_import_dict(self, values, model=None):
        # we disable enderEmit related creation with dry_run=True
        context = self._context.copy()
        context['dry_run'] = True
        values = super(
            ResCompany,
            self.with_context(context)
        )._prepare_import_dict(values, model)
        if not values.get('name'):
            values['name'] = (values.get('nfe40_xNome')
                              or values.get('nfe40_xFant'))
        return values
