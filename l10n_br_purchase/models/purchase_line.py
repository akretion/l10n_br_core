# Copyright (C) 2009  Renato Lima - Akretion, Gabriel C. Stabel
# Copyright (C) 2012  Raphaël Valyi - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PurchaseOrderLine(models.Model):
    _name = 'purchase.order.line'
    _inherit = ['purchase.order.line', 'l10n_br_fiscal.document.line.mixin']

    @api.onchange('product_id')
    def onchange_product_id(self):

        # Todo - original code returns error because it call map_tax
        #   without inform product parameter, to test just remove the
        #   SUPER at the end of the method.
        #   By this reason I need to bring original code here.
        result = {}
        if not self.product_id:
            return result

        # Reset date, price and quantity since
        # _onchange_quantity will provide default values
        self.date_planned = datetime.today().strftime(
            DEFAULT_SERVER_DATETIME_FORMAT)
        self.price_unit = self.product_qty = 0.0
        self.product_uom = \
            self.product_id.uom_po_id or self.product_id.uom_id
        result['domain'] = {
            'product_uom': [(
                'category_id', '=', self.product_id.uom_id.category_id.id)]}

        product_lang = self.product_id.with_context(
            lang=self.partner_id.lang,
            partner_id=self.partner_id.id,
        )
        self.name = product_lang.display_name
        if product_lang.description_purchase:
            self.name += '\n' + product_lang.description_purchase

        # Part of the original code cause error

        # fpos = self.order_id.fiscal_position_id
        # if self.env.uid == SUPERUSER_ID:
        #    company_id = self.env.user.company_id.id
        #
        #    self.taxes_id = fpos.map_tax(
        #    self.product_id.supplier_taxes_id.filtered(
        #    lambda r: r.company_id.id == company_id))
        # else:
        #    self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id)

        self._suggest_quantity()
        self._onchange_quantity()

        context = dict(self.env.context)

        result = {'value': {}}
        result['value']['invoice_state'] = context.get('parent_invoice_state')

        if (self.order_id.fiscal_category_id
                and self.product_id and self.partner_id):
            result = {'value': {}}
            kwargs = {
                'company_id': self.order_id.company_id,
                'partner_id': self.order_id.partner_id,
                'partner_invoice_id': self.order_id.partner_id,
                'partner_shipping_id': self.order_id.dest_address_id,
                'product_id': self.product_id,
                'fiscal_category_id': self.fiscal_category_id or
                self.order_id.fiscal_category_id,
                'context': self.env.context
            }
            result.update(self._fiscal_position_map(**kwargs))

            self.update(result['value'])

        # Remove comment of line below to see the error
        # result_super = super(PurchaseOrderLine, self).onchange_product_id()
        # if result_super.get('value'):
        #     result_super.get('value').update(result['value'])
        # else:
        #     result_super.update(result)
        # return result_super

        return result

    @api.multi
    @api.onchange('fiscal_category_id', 'fiscal_position_id')
    def onchange_fiscal(self):
        for record in self:
            if record.product_id and record.order_id.company_id and\
                    record.order_id.partner_id and record.fiscal_category_id:
                result = {'value': {}}
                kwargs = {
                    'company_id': record.order_id.company_id,
                    'partner_id': record.order_id.partner_id,
                    'partner_invoice_id': record.order_id.partner_id,
                    'partner_shipping_id': record.order_id.dest_address_id,
                    'product_id': record.product_id,
                    'fiscal_category_id': record.fiscal_category_id or
                    record.order_id.fiscal_category_id,
                    'context': record.env.context
                }
                result.update(self._fiscal_position_map(**kwargs))

                record.update(result['value'])

    @api.multi
    def _prepare_stock_moves(self, picking):
        """
        Prepare the stock moves data for one order line.
         This function returns a list of
        dictionary ready to be used in stock.move's create()
        """
        self.ensure_one()
        vals = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        vals[0].update({
            'fiscal_category_id': self.fiscal_category_id.id,
            'fiscal_position_id': self.fiscal_position_id.id,
        })
        return vals
