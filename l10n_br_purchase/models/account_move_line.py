# Copyright (C) 2021  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _prepare_account_move_line(self, move):
        values = super()._prepare_account_move_line(move)
        if values.get("purchase_line_id"):
            line = self.env["purchase.order.line"].browse(
                values.get("purchase_line_id")
            )
            fiscal_values = line._prepare_br_fiscal_dict()
            fiscal_values.update(values)
            values.update(fiscal_values)

        return values
