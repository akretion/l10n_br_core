# Copyright 2021 Akretion - Raphaël Valyi <raphael.valyi@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import base64
import os

from odoo import tools
from odoo.modules import get_resource_path
from odoo.tests import common


class TestReturnImport(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.company_a = self.browse_ref("base.main_company")
        tools.convert_file(
            self.cr,
            "account",
            get_resource_path("account", "test", "account_minimal_test.xml"),
            {},
            "init",
            False,
            "test",
        )
        self.account_move_obj = self.env["account.move"]
        self.account_move_line_obj = self.env["account.move.line"]
        self.cnab_log_obj = self.env["l10n_br_cnab.return.log"]
        self.account_id = self.ref("account.a_recv")
        self.bank_account = self.browse_ref("account.bnk")
        self.journal = self.browse_ref("account.bank_journal")
        self.import_wizard_obj = self.env["credit.statement.import"]
        self.partner = self.browse_ref("base.res_partner_12")
        self.journal.write(
            {
                "used_for_import": True,
                "import_type": "cnab400",
                "partner_id": self.partner.id,
                "commission_account_id": self.account_id,
                "receivable_account_id": self.account_id,
                "create_counterpart": True,
                "bank_account_id": self.ref(
                    "l10n_br_account_payment_order.main_company_bank_unicredi"
                ),
            }
        )

    def _import_file(self, file_name):
        """import a file using the wizard
        return the create account.bank.statement object
        """
        with open(file_name, "rb") as f:
            content = f.read()
            self.wizard = self.import_wizard_obj.create(
                {
                    "journal_id": self.journal.id,
                    "input_statement": base64.b64encode(content),
                    "file_name": os.path.basename(file_name),
                }
            )
            action = self.wizard.import_statement()
            log_view_ref = self.ref(
                "l10n_br_account_payment_order.l10n_br_cnab_return_log_form_view"
            )
            if action["views"] == [(log_view_ref, "form")]:
                return self.cnab_log_obj.browse(action["res_id"])
            else:
                return self.account_move_obj.browse(action["res_id"])

    def test_valor_menor_1(self):
        file_name = get_resource_path(
            "l10n_br_account_payment_brcobranca",
            "tests",
            "CNAB400UNICRED_valor_menor_1.RET",
        )
        log = self._import_file(file_name)
        self.assertEqual("Banco UNICRED - Conta 371", log.name)

    def test_valor_menor_2(self):
        file_name = get_resource_path(
            "l10n_br_account_payment_brcobranca",
            "tests",
            "CNAB400UNICRED_valor_menor_2.RET",
        )
        log = self._import_file(file_name)
        self.assertEqual("Banco UNICRED - Conta 371", log.name)

    def test_valor_maior_3(self):
        file_name = get_resource_path(
            "l10n_br_account_payment_brcobranca",
            "tests",
            "CNAB400UNICRED_valor_maior_3.RET",
        )
        log = self._import_file(file_name)
        self.assertEqual("Banco UNICRED - Conta 371", log.name)

    def test_valor_maior_4(self):
        file_name = get_resource_path(
            "l10n_br_account_payment_brcobranca",
            "tests",
            "CNAB400UNICRED_valor_maior_4.RET",
        )
        log = self._import_file(file_name)
        self.assertEqual("Banco UNICRED - Conta 371", log.name)
