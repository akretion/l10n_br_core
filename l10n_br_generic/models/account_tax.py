# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountTax(models.Model):
    """ Add fields used to define some brazilian taxes """
    _inherit = 'account.tax'

    tax_discount = fields.Boolean(
        string='Discount this Tax in Prince',
		related='tax_group_id.tax_discount',
        help="Mark it for (ICMS, PIS e etc.).")

    domain = fields.Selection(
        related='tax_group_id.domain',
        string='Tax Domain')

    base_reduction = fields.Float(
        string='Redution',
        digits=0,
        default=0,
        required=True,
        help="Um percentual decimal em % entre 0-1.")

    amount_mva = fields.Float(
        string='MVA Percent',
        digits=0,
        default=0,
        required=True,
        help="Um percentual decimal em % entre 0-1.")
