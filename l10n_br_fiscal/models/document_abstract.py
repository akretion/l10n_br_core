# Copyright (C) 2019  Renato Lima - Akretion <renato.lima@akretion.com.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api

from odoo.addons.l10n_br_base.tools import fiscal, misc

from ..constants.fiscal import TAX_FRAMEWORK


class DocumentAbstract(models.AbstractModel):
    _name = 'l10n_br_fiscal.document.abstract'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'format.address.mixin']
    _description = 'Fiscal Document Abstract'

    @api.one
    @api.depends('line_ids')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.amount_untaxed
                                  for line in self.line_ids)
        self.amount_tax = sum(line.amount_tax for line in self.line_ids)
        self.amount_discount = sum(line.discount
                                   for line in self.line_ids)
        self.amount_total = sum(line.amount_total for line in self.line_ids)

    number = fields.Char(
        string='Number',
        required=True,
        index=True)

    key = fields.Char(
        string='key',
        required=True,
        index=True)

    document_type_id = fields.Many2one(
        comodel_name='l10n_br_fiscal.document.type',
        required=True)

    document_electronic = fields.Boolean(
        related='document_type_id.electronic',
        string='Electronic?')

    date = fields.Date(
        string='Date')

    date_in_out = fields.Datetime(
        string='Date Move')

    document_serie_id = fields.Many2one(
        comodel_name='l10n_br_fiscal.document.serie',
        domain="[('active', '=', True),"
               "('document_type_id', '=', document_type_id)]",
        required=True)

    document_serie = fields.Char(
        string='Serie Number')

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner')

    partner_legal_name = fields.Char(
        string='Legal Name')

    partner_name = fields.Char(
        string='Name')

    partner_cnpj_cpf = fields.Char(
        string='CNPJ')

    partner_inscr_est = fields.Char(
        string='State Tax Number')

    partner_inscr_mun = fields.Char(
        string='Municipal Tax Number')

    partner_suframa = fields.Char(
        string='Suframa')

    partner_cnae_main_id = fields.Many2one(
        comodel_name='l10n_br_fiscal.cnae',
        string='Main CNAE')

    partner_tax_framework = fields.Selection(
        selection=TAX_FRAMEWORK,
        string='Tax Framework')

    partner_shipping_id = fields.Many2one(
        comodel_name='res.partner',
        string='Shipping Address')

    operation_id = fields.Many2one(
        comodel_name='l10n_br_fiscal.operation',
        string='Operation')

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'l10n_br_fiscal.tax.estimate'))

    company_legal_name = fields.Char(
        string='Legal Name',
        related='company_id.legal_name')

    company_name = fields.Char(
        string='Name',
        related='company_id.name',
        size=128)

    company_cnpj_cpf = fields.Char(
        string='CNPJ',
        related='company_id.cnpj_cpf')

    company_inscr_est = fields.Char(
        string='State Tax Number',
        related='company_id.inscr_est')

    company_inscr_mun = fields.Char(
        string='Municipal Tax Number',
        related='company_id.inscr_mun')

    company_suframa = fields.Char(
        string='Suframa',
        related='company_id.suframa')

    company_cnae_main_id = fields.Many2one(
        comodel_name='l10n_br_fiscal.cnae',
        related='company_id.cnae_main_id',
        string='Main CNAE')

    company_tax_framework = fields.Selection(
        selection=TAX_FRAMEWORK,
        related='company_id.tax_framework',
        string='Tax Framework')

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.currency_id',
        store=True,
        readonly=True)

    amount_untaxed = fields.Monetary(
        string="Amount Untaxed",
        compute='_compute_amount')

    amount_tax = fields.Monetary(
        string="Amount Tax",
        compute='_compute_amount')

    amount_total = fields.Monetary(
        string="Amount Total",
        compute='_compute_amount')

    amount_discount = fields.Monetary(
        string="Amount Discount",
        compute='_compute_amount')

    line_ids = fields.One2many(
        comodel_name='l10n_br_fiscal.document.line.abstract',
        inverse_name='document_id',
        string='Document Lines')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_legal_name = self.partner_id.legal_name
            self.partner_name = self.partner_id.name
            self.partner_cnpj_cpf = self.partner_id.cnpj_cpf
            self.partner_inscr_est = self.partner_id.inscr_est
            self.partner_inscr_mun = self.partner_id.inscr_mun
            self.partner_suframa = self.partner_id.suframa
            self.partner_cnae_main_id = self.partner_id.cnae_main_id
            self.partner_tax_framework = self.partner_id.tax_framework

    @api.onchange('partner_cnpj_cpf', 'country_id')
    def _onchange_partner_cnpj_cpf(self):
        country = self.country_id.code or ''
        self.cnpj_cpf = fiscal.format_cpf_cnpj(self.cnpj_cpf,
                                               country,
                                               self.partner_id.is_company)

    @api.onchange('zip')
    def _onchange_zip(self):
        self.zip = misc.format_zipcode(self.zip,
                                       self.country_id.code)
