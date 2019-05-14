# Copyright 2019 Akretion - Renato Lima <renato.lima@akretion.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo.tests import common
from odoo import fields


class TestIbptProduct(common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.company_model = self.env['res.company']
        self.company = self._create_compay()
        self.ncm_85030010 = self.env.ref('fiscal.ncm_85030010')
        self.ncm_85014029 = self.env.ref('fiscal.ncm_85014029')
        self.product_tmpl_model = self.env['product.template']
        self.product_tmpl_1 = self._create_product_tmpl_1()
        self.product_tmpl_2 = self._create_product_tmpl_2()
        self.product_tmpl_3 = self._create_product_tmpl_3()
        self.fiscal_tax_estimate_model = self.env['fiscal.tax.estimate']
        self.fiscal_ncm_model = self.env['fiscal.ncm']

    def _create_compay(self):
        # Creating a company
        company = self.env.ref('base.main_company').write({
            'cnpj_cpf': '02.960.895/0002-12',
            'country_id': self.env.ref('base.br').id,
            'state_id': self.env.ref('base.state_br_es').id,
            'ibpt_api': True,
            'ibpt_update_days': 0,
            'ibpt_token': ('dsaaodNP5i6RCu007nPQjiOPe5XIefnx'
                           'StS2PzOV3LlDRVNGdVJ5OOUlwWZhjFZk')
        })
        return company

    def _create_product_tmpl_1(self):
        # Creating a product
        product = self.product_tmpl_model.create({
            'name': 'Product Test 1 - With NCM: 8503.00.10',
            'ncm_id': self.ncm_85030010.id
        })
        return product

    def _create_product_tmpl_2(self):
        # Creating a product
        product = self.product_tmpl_model.create({
            'name': 'Product Test 2 - With NCM: 8503.00.10',
            'ncm_id': self.ncm_85030010.id
        })
        return product

    def _create_product_tmpl_3(self):
        # Creating a product
        product = self.product_tmpl_model.create({
            'name': 'Product Test 3 - With NCM: 8501.40.29',
            'ncm_id': self.ncm_85014029.id
        })
        return product

    def test_update_ibpt_product(self):
        """Check tax estimate update"""
        self.ncm_85030010.get_ibpt()
        self.assertTrue(self.ncm_85030010.tax_estimate_ids)

        self.ncm_85014029.get_ibpt()
        self.assertTrue(self.ncm_85014029.tax_estimate_ids)

        tax_estimates = self.fiscal_tax_estimate_model.search([
            ('ncm_id', 'in', (self.ncm_85030010.id, self.ncm_85014029.id))
        ]).unlink()

    def test_ncm_count_product_template(self):
        """Check product template relation with NCM"""
        self.assertEquals(self.ncm_85030010.product_tmpl_qty, 2)
        self.assertEquals(self.ncm_85014029.product_tmpl_qty, 1)

    def test_update_scheduled(self):
        """Check NCM update scheduled"""
        ncms = self.fiscal_ncm_model.search([
            ('id', 'in', (self.ncm_85030010.id, self.ncm_85014029.id))])
        ncms._scheduled_update()

        self.assertTrue(self.ncm_85030010.tax_estimate_ids)
        self.assertTrue(self.ncm_85014029.tax_estimate_ids)

        tax_estimates = self.fiscal_tax_estimate_model.search([
            ('ncm_id', 'in', (self.ncm_85030010.id, self.ncm_85014029.id))
        ]).unlink()
