# Copyright (C) 2009  Renato Lima - Akretion, Gabriel C. Stabel
# Copyright (C) 2012  Raphaël Valyi - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'l10n_br_fiscal.document.mixin']

    @api.model
    def _prepare_picking(self):
        values = super(PurchaseOrder, self)._prepare_picking()
        values.update({
            'operation_id': (self.operation_id.id),
        })
        return values
