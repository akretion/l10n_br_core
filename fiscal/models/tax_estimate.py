# Copyright (C) 2012  Renato Lima - Akretion <renato.lima@akretion.com.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields
from odoo.exceptions import ValidationError

from odoo.addons import decimal_precision as dp


class TaxEstimate(models.Model):
    _name = 'fiscal.tax.estimate'
    _description = 'Fiscal Tax Estimate'

    ncm_id = fields.Many2one(
        comodel_name='fiscal.ncm',
        string=u'NCM',
        required=True)

    nbs_id = fields.Many2one(
        comodel_name='fiscal.nbs',
        string=u'NBS',
        required=True)

    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string=u'Estado',
        required=True)

    federal_taxes_national = fields.Float(
        string=u'Impostos Federais Nacional',
        default=0.00,
        digits=dp.get_precision('Fiscal Tax Percent'))

    federal_taxes_import = fields.Float(
        string='Impostos Federais Importado',
        default=0.00,
        digits=dp.get_precision('Fiscal Tax Percent'))

    state_taxes = fields.Float(
        string='Impostos Estaduais Nacional',
        default=0.00,
        digits=dp.get_precision('Fiscal Tax Percent'))

    municipal_taxes = fields.Float(
        string='Impostos Municipais Nacional',
        default=0.00,
        digits=dp.get_precision('Fiscal Tax Percent'))

    create_date = fields.Datetime(
        string=u'Data de Criação',
        readonly=True)

    key = fields.Char(
        string='Chave',
        size=32)

    origin = fields.Char(
        string='Fonte',
        size=32)
