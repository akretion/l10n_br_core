# @ 2020 KMEE - www.kmee.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase

from odoo.addons.l10n_br_base.tests.tools import load_fixture_files

from .tools import load_fiscal_fixture_files


class TestSubsequentOperation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_fiscal_fixture_files(cls.env)
        load_fixture_files(
            cls.env, "l10n_br_fiscal", file_names=["subsequent_operation_demo.xml"]
        )

        cls.nfe_simples_faturamento = cls.env.ref(
            "l10n_br_fiscal.demo_nfe_so_simples_faturamento"
        ).copy()

        cls.so_simples_faturamento = cls.env.ref(
            "l10n_br_fiscal.so_simples_faturamento"
        )

        cls.tax_icms_12 = cls.env.ref("l10n_br_fiscal.tax_icms_12")
        cls.pis_tax_0 = cls.env.ref("l10n_br_fiscal.tax_pis_0")
        cls.cofins_tax_0 = cls.env.ref("l10n_br_fiscal.tax_cofins_0")

    def test_subsequent_operation_simple_faturamento(self):
        """Test Fiscal Subsequent Operation Simples Faturamento"""

        self.nfe_simples_faturamento._onchange_fiscal_operation_id()
        self.nfe_simples_faturamento._onchange_document_serie_id()

        for line in self.nfe_simples_faturamento.fiscal_line_ids:
            line._onchange_product_id_fiscal()
            line._onchange_fiscal_taxes()

        self.nfe_simples_faturamento.state_edoc = "a_enviar"
        self.nfe_simples_faturamento._generates_subsequent_operations()

        subsequent_documents = self.nfe_simples_faturamento.document_subsequent_ids

        for document in subsequent_documents:
            self.assertTrue(
                document.subsequent_document_id, "Subsequent document was not created"
            )

            # Subsequent Document operation
            self.assertEqual(
                document.subsequent_document_id.fiscal_operation_id.id,
                self.so_simples_faturamento.subsequent_operation_id.id,
                "Operation of the generated document is incorrect",
            )

            # Subsequent Lines
            for product in document.subsequent_document_id.fiscal_line_ids:
                # Document Line ICMS tax
                self.assertEqual(
                    product.icms_tax_id.id,
                    self.tax_icms_12.id,
                    "ICMS tax value is not 12%",
                )

                # Document Line PIS tax
                self.assertEqual(
                    product.pis_tax_id.id, self.pis_tax_0.id, "PIS tax value is not 0%"
                )

                # Document Line COFINS tax
                self.assertEqual(
                    product.cofins_tax_id.id,
                    self.cofins_tax_0.id,
                    "COFINS tax value is not 0%",
                )
