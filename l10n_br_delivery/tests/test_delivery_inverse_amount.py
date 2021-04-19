# @ 2020 KMEE - www.kmee.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase, Form


class TestDeliveryInverseAmount(SavepointCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()

        self.sale_demo = self.env.ref('l10n_br_sale.main_so_delivery_costs_1')

        # Create two sale orders
        sale_order_form_total = Form(self.env['sale.order'], 'sale.view_order_form')
        sale_order_form_total.partner_id = self.env.ref(
            'l10n_br_base.res_partner_kmee')
        self.sale_order_total_id = sale_order_form_total.save()

        sale_order_form_line = Form(self.env['sale.order'], 'sale.view_order_form')
        sale_order_form_line.partner_id = self.env.ref(
            'l10n_br_base.res_partner_kmee')
        self.sale_order_line_id = sale_order_form_line.save()

        # Set 2 different products to the sale orders
        with Form(self.sale_order_total_id) as so:
            with so.order_line.new() as line:
                line.product_id = self.env.ref('product.product_delivery_01')
            with so.order_line.new() as line:
                line.product_id = self.env.ref('product.product_delivery_02')

        with Form(self.sale_order_line_id) as so:
            with so.order_line.new() as line:
                line.product_id = self.env.ref('product.product_delivery_01')
            with so.order_line.new() as line:
                line.product_id = self.env.ref('product.product_delivery_02')

        # Change freight, insurance and other costs amount from
        # sale_order_total_id
        with Form(self.sale_order_total_id) as so:
            so.amount_freight_value = 100.0
            so.amount_insurance_value = 100.0
            so.amount_other_value = 100.0

        # Change freight, insurance and other costs amount from
        # sale_order_lines_id lines
        # TODO ?: alterando para permitir edição do campo e não falhar o teste
        self.sale_order_line_id.company_id.delivery_costs = 'line'
        with Form(self.sale_order_line_id) as so:
            with so.order_line.edit(0) as line:
                line.freight_value = 70.00
                line.insurance_value = 70.00
                line.other_value = 70.00
            with so.order_line.edit(1) as line:
                line.freight_value = 10.00
                line.insurance_value = 10.00
                line.other_value = 10.00

        # TODO ?: alterando para permitir edição do campo e não falhar o teste
        self.sale_order_line_id.company_id.delivery_costs = 'total'
        with Form(self.sale_order_line_id) as so:
            so.amount_freight_value = 100.0
            so.amount_insurance_value = 100.0
            so.amount_other_value = 100.0

        # Confirm and create invoices for the sale orders
        self.sale_order_total_id.action_confirm()
        self.sale_order_line_id.action_confirm()

        for move in self.sale_order_total_id.picking_ids.mapped(
                'move_ids_without_package'):
            move.quantity_done = move.product_uom_qty

        for move in self.sale_order_line_id.picking_ids.mapped(
                'move_ids_without_package'):
            move.quantity_done = move.product_uom_qty

        for picking in self.sale_order_total_id.picking_ids.filtered(
                lambda p: p.state == 'confirmed'):
            picking.button_validate()

        for picking in self.sale_order_line_id.picking_ids.filtered(
                lambda p: p.state == 'confirmed'):
            picking.button_validate()

        wizard_total = self.env['sale.advance.payment.inv'].with_context(
            {'active_ids': self.sale_order_total_id.ids}).create({})

        wizard_line = self.env['sale.advance.payment.inv'].with_context(
            {'active_ids': self.sale_order_line_id.ids}).create({})

        wizard_total.create_invoices()
        wizard_line.create_invoices()

    def test_sale_order_total_amounts(self):
        """Check sale order total amounts"""
        self.assertEqual(
            self.sale_order_total_id.amount_price_gross, 110.0,
            "Unexpected value for the field amount_price_gross from Sale Order")
        self.assertEqual(
            self.sale_order_total_id.amount_untaxed, 110.0,
            "Unexpected value for the field amount_untaxed from Sale Order")
        self.assertEqual(
            self.sale_order_total_id.amount_freight_value, 100.0,
            "Unexpected value for the field amount_freight from Sale Order")
        self.assertEqual(
            self.sale_order_total_id.amount_insurance_value, 100.0,
            "Unexpected value for the field amount_insurance from Sale Order")
        self.assertEqual(
            self.sale_order_total_id.amount_other_value, 100.0,
            "Unexpected value for the field amount_costs from Sale Order")
        self.assertEqual(
            self.sale_order_total_id.amount_tax, 0.0,
            "Unexpected value for the field amount_tax from Sale Order")

    def test_sale_order_line_amounts(self):
        """Check sale order line amounts"""
        self.assertEqual(
            self.sale_order_line_id.amount_price_gross, 110.0,
            "Unexpected value for the field amount_price_gross from Sale Order")
        self.assertEqual(
            self.sale_order_line_id.amount_untaxed, 110.0,
            "Unexpected value for the field amount_untaxed from Sale Order")
        self.assertEqual(
            self.sale_order_line_id.amount_freight_value, 100.0,
            "Unexpected value for the field amount_freight from Sale Order")
        self.assertEqual(
            self.sale_order_line_id.amount_insurance_value, 100.0,
            "Unexpected value for the field amount_insurance from Sale Order")
        self.assertEqual(
            self.sale_order_line_id.amount_other_value, 100.0,
            "Unexpected value for the field amount_other from Sale Order")
        self.assertEqual(
            self.sale_order_line_id.amount_tax, 0.0,
            "Unexpected value for the field amount_tax from Sale Order")

    def test_invoice_amount_tax(self):
        """Check invoice amount tax"""
        invoice_tax_total = self.sale_order_total_id.invoice_ids[0].amount_tax

        self.assertEqual(
            invoice_tax_total, 0.0,
            "Unexpected value for the field invoice_tax from Invoice")

        invoice_tax_line = self.sale_order_line_id.invoice_ids[0].amount_tax

        self.assertEqual(
            invoice_tax_line, 0.0,
            "Unexpected value for the field invoice_tax from Invoice")

    def test_inverse_amount_freight_total(self):
        """Check Fiscal Document freight values for total"""
        fiscal_document_id = \
            self.sale_order_total_id.invoice_ids[0].fiscal_document_id
        self.assertEqual(
            fiscal_document_id.amount_freight_value, 100,
            "Unexpected value for the field amount_freight_value from "
            "Fiscal Document")

        for line in fiscal_document_id.line_ids:
            if line.name == '[FURN_7777] Office Chair':
                self.assertEqual(
                    line.freight_value, 63.64,
                    "Unexpected value for the field freight_value from "
                    "Fiscal Document line")
            if line.name == '[FURN_8888] Office Lamp':
                self.assertEqual(
                    line.freight_value, 36.36,
                    "Unexpected value for the field freight_value from "
                    "Fiscal Document line")

        # TODO ? : O documento fiscal so permite os valores serem informados
        #  por linha, pendente wizard p/ informar total e ratear por linhas
        # with Form(fiscal_document_id) as doc:
        #    doc.amount_freight_value = 10.0

        # for line in fiscal_document_id.line_ids:
        #     if line.name == '[FURN_7777] Office Chair':
        #         self.assertEqual(
        #             line.freight_value, 6.36,
        #             "Unexpected value for the field freight_value from "
        #             "Fiscal Document line")
        #     if line.name == '[FURN_8888] Office Lamp':
        #         self.assertEqual(
        #             line.freight_value, 3.64,
        #             "Unexpected value for the field freight_value from "
        #             "Fiscal Document line")

    def test_inverse_amount_freight_line(self):
        """Check Fiscal Document freight values for lines"""
        fiscal_document_id = \
            self.sale_order_line_id.invoice_ids[0].fiscal_document_id
        self.assertEqual(
            fiscal_document_id.amount_freight_value, 100,
            "Unexpected value for the field amount_freight_value from "
            "Fiscal Document")

        for line in fiscal_document_id.line_ids:
            if line.name == '[FURN_7777] Office Chair':
                self.assertEqual(
                    line.freight_value, 87.5,
                    "Unexpected value for the field freight_value from "
                    "Fiscal Document line")
            if line.name == '[FURN_8888] Office Lamp':
                self.assertEqual(
                    line.freight_value, 12.5,
                    "Unexpected value for the field freight_value from "
                    "Fiscal Document line")

        # TODO ? : O documento fiscal so permite os valores serem informados
        #  por linha, pendente wizard p/ informar total e ratear por linhas
        # with Form(fiscal_document_id) as doc:
        #     doc.amount_freight_value = 10.0

        # for line in fiscal_document_id.line_ids:
        #     if line.name == '[FURN_7777] Office Chair':
        #         self.assertEqual(
        #             line.freight_value, 8.75,
        #             "Unexpected value for the field freight_value from "
        #             "Fiscal Document line")
        #     if line.name == '[FURN_8888] Office Lamp':
        #         self.assertEqual(
        #             line.freight_value, 1.25,
        #             "Unexpected value for the field freight_value from "
        #             "Fiscal Document line")

    def test_inverse_amount_insurance_total(self):
        """Check Fiscal Document insurance values for total"""
        fiscal_document_id = \
            self.sale_order_total_id.invoice_ids[0].fiscal_document_id
        self.assertEqual(
            fiscal_document_id.amount_insurance_value, 100,
            "Unexpected value for the field amount_insurance_value from "
            "Fiscal Document")

        for line in fiscal_document_id.line_ids:
            if line.name == '[FURN_7777] Office Chair':
                self.assertEqual(
                    line.insurance_value, 63.64,
                    "Unexpected value for the field insurance_value from "
                    "Fiscal Document line")
            if line.name == '[FURN_8888] Office Lamp':
                self.assertEqual(
                    line.insurance_value, 36.36,
                    "Unexpected value for the field insurance_value from "
                    "Fiscal Document line")

        # TODO ? : O documento fiscal so permite os valores serem informados
        #  por linha, pendente wizard p/ informar total e ratear por linhas
        # with Form(fiscal_document_id) as doc:
        #    doc.amount_insurance_value = 10.0

        # for line in fiscal_document_id.line_ids:
        #     if line.name == '[FURN_7777] Office Chair':
        #         self.assertEqual(
        #             line.insurance_value, 6.36,
        #             "Unexpected value for the field insurance_value from "
        #             "Fiscal Document line")
        #     if line.name == '[FURN_8888] Office Lamp':
        #         self.assertEqual(
        #             line.insurance_value, 3.64,
        #             "Unexpected value for the field insurance_value from "
        #             "Fiscal Document line")

    def test_inverse_amount_insurance_line(self):
        """Check Fiscal Document insurance values for lines"""
        fiscal_document_id = \
            self.sale_order_line_id.invoice_ids[0].fiscal_document_id
        self.assertEqual(
            fiscal_document_id.amount_insurance_value, 100,
            "Unexpected value for the field amount_insurance_value from "
            "Fiscal Document")

        for line in fiscal_document_id.line_ids:
            if line.name == '[FURN_7777] Office Chair':
                self.assertEqual(
                    line.insurance_value, 87.5,
                    "Unexpected value for the field insurance_value from "
                    "Fiscal Document line")
            if line.name == '[FURN_8888] Office Lamp':
                self.assertEqual(
                    line.insurance_value, 12.5,
                    "Unexpected value for the field insurance_value from "
                    "Fiscal Document line")

        # TODO ? : O documento fiscal so permite os valores serem informados
        #  por linha, pendente wizard p/ informar total e ratear por linhas
        # with Form(fiscal_document_id) as doc:
        #    doc.amount_insurance_value = 10.0

        # for line in fiscal_document_id.line_ids:
        #     if line.name == '[FURN_7777] Office Chair':
        #         self.assertEqual(
        #             line.insurance_value, 8.75,
        #             "Unexpected value for the field insurance_value from "
        #             "Fiscal Document line")
        #     if line.name == '[FURN_8888] Office Lamp':
        #         self.assertEqual(
        #             line.insurance_value, 1.25,
        #             "Unexpected value for the field insurance_value from "
        #             "Fiscal Document line")

    def test_inverse_amount_other_costs_total(self):
        """Check Fiscal Document other costs values for total"""
        fiscal_document_id = \
            self.sale_order_total_id.invoice_ids[0].fiscal_document_id
        self.assertEqual(
            fiscal_document_id.amount_other_value, 100,
            "Unexpected value for the field other_value from "
            "Fiscal Document")

        for line in fiscal_document_id.line_ids:
            if line.name == '[FURN_7777] Office Chair':
                self.assertEqual(
                    line.other_value, 63.64,
                    "Unexpected value for the field other_value from "
                    "Fiscal Document line")
            if line.name == '[FURN_8888] Office Lamp':
                self.assertEqual(
                    line.other_value, 36.36,
                    "Unexpected value for the field other_value from "
                    "Fiscal Document line")

        # TODO ? : O documento fiscal so permite os valores serem informados
        #  por linha, pendente wizard p/ informar total e ratear por linhas
        # with Form(fiscal_document_id) as doc:
        #    doc.amount_other_value = 10.0

        # for line in fiscal_document_id.line_ids:
        #     if line.name == '[FURN_7777] Office Chair':
        #         self.assertEqual(
        #             line.other_value, 6.36,
        #             "Unexpected value for the field other_value from "
        #             "Fiscal Document line")
        #     if line.name == '[FURN_8888] Office Lamp':
        #         self.assertEqual(
        #             line.other_value, 3.64,
        #             "Unexpected value for the field other_value from "
        #             "Fiscal Document line")

    def test_inverse_amount_other_line(self):
        """Check Fiscal Document other other values for lines"""
        fiscal_document_id = \
            self.sale_order_line_id.invoice_ids[0].fiscal_document_id
        self.assertEqual(
            fiscal_document_id.amount_other_value, 100,
            "Unexpected value for the field other_value from "
            "Fiscal Document")

        for line in fiscal_document_id.line_ids:
            if line.name == '[FURN_7777] Office Chair':
                self.assertEqual(
                    line.other_value, 87.5,
                    "Unexpected value for the field other_value from "
                    "Fiscal Document line")
            if line.name == '[FURN_8888] Office Lamp':
                self.assertEqual(
                    line.other_value, 12.5,
                    "Unexpected value for the field other_value from "
                    "Fiscal Document line")

        # TODO ? : O documento fiscal so permite os valores serem informados
        #  por linha, pendente wizard p/ informar total e ratear por linhas
        # with Form(fiscal_document_id) as doc:
        #    doc.amount_other_value = 10.0

        # for line in fiscal_document_id.line_ids:
        #     if line.name == '[FURN_7777] Office Chair':
        #         self.assertEqual(
        #             line.other_value, 8.75,
        #             "Unexpected value for the field other_value from "
        #             "Fiscal Document line")
        #     if line.name == '[FURN_8888] Office Lamp':
        #         self.assertEqual(
        #             line.other_value, 1.25,
        #             "Unexpected value for the field other_value from "
        #             "Fiscal Document line")

    def test_not_cost_ratio_by_lines(self):
        """
        Teste quando não deve acontecer divisão proporcional entre os valores,
        de Frete, Seguro e Outros Custos, esses valores nas linhas devem ser
        independentes.
        """
        self.sale_demo.company_id.delivery_costs = 'line'
        self.sale_demo.action_confirm()

        self.assertEqual(
            self.sale_demo.amount_freight_value, 30.0,
            'Unexpected value for the field amount_freight from Sale Order')
        self.assertEqual(
            self.sale_demo.amount_insurance_value, 45.0,
            'Unexpected value for the field amount_insurance from Sale Order')
        self.assertEqual(
            self.sale_demo.amount_other_value, 15.0,
            'Unexpected value for the field amount_costs from Sale Order')
        for l in self.sale_demo.order_line:
            other_line = self.sale_demo.order_line.filtered(
                lambda o_l: o_l.id != l.id )
            self.assertNotEqual(
                l.freight_value, other_line.freight_value,
                'Value freight_value should not be has same value in lines.')
            self.assertNotEqual(
                l.insurance_value, other_line.insurance_value,
                'Value insurance_value should not be has same value in lines.')
            self.assertNotEqual(
                l.other_value, other_line.other_value,
                'Value other_value should not be has same value in lines.')

        picking = self.sale_demo.picking_ids
        # Check product availability
        picking.action_assign()
        # Force product availability
        for move in picking.move_ids_without_package:
            move.quantity_done = move.product_uom_qty
        picking.button_validate()
        self.assertEqual(picking.state, 'done')

        self.sale_demo.action_invoice_create(final=True)

        self.assertEquals(
            self.sale_demo.state, 'sale', 'Error to confirm Sale Order.'
        )

        invoice = self.sale_demo.invoice_ids[0]
        invoice.action_invoice_open()
        self.assertEquals(
            invoice.state, "open", "Invoice should be in state Open"
        )
        for l in invoice.invoice_line_ids:
            other_line = invoice.invoice_line_ids.filtered(
                lambda o_l: o_l.id != l.id )
            self.assertNotEqual(
                l.freight_value, other_line.freight_value,
                'Value freight_value should not be has same value'
                ' in invoice lines.')
            self.assertNotEqual(
                l.insurance_value, other_line.insurance_value,
                'Value insurance_value should not be has same value'
                ' in invoice lines.')
            self.assertNotEqual(
                l.other_value, other_line.other_value,
                'Value other_value should not be has same value'
                ' in invoice lines.')

        fiscal_document_id = \
            self.sale_demo.invoice_ids[0].fiscal_document_id

        for l in fiscal_document_id.line_ids:
            other_line = fiscal_document_id.line_ids.filtered(
                lambda o_l: o_l.id != l.id )
            self.assertNotEqual(
                l.freight_value, other_line.freight_value,
                'Value freight_value should not be has same value'
                ' in invoice lines.')
            self.assertNotEqual(
                l.insurance_value, other_line.insurance_value,
                'Value insurance_value should not be has same value'
                ' in invoice lines.')
            self.assertNotEqual(
                l.other_value, other_line.other_value,
                'Value other_value should not be has same value'
                ' in invoice lines.')
