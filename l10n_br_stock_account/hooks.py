# Copyright (C) 2020  Renato Lima - Akretion <renato.lima@akretion.com.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging

from odoo import SUPERUSER_ID, _, api, tools

from odoo.addons.l10n_br_fiscal.tools import inform_journal_in_fiscal_operation

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    if not tools.config["without_demo"]:
        _logger.info(_("Loading l10n_br_stock_account/demo/company_demo.xml ..."))
        tools.convert_file(
            cr,
            "l10n_br_stock_account",
            "demo/company_demo.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )
        _logger.info(
            _("Loading l10n_br_stock_account/demo/l10n_br_stock_account_demo.xml ...")
        )
        tools.convert_file(
            cr,
            "l10n_br_stock_account",
            "demo/l10n_br_stock_account_demo.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )
        _logger.info(
            _("Loading l10n_br_stock_account/demo/account_journal_demo.xml ...")
        )
        tools.convert_file(
            cr,
            "l10n_br_stock_account",
            "demo/account_journal_demo.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )
        _logger.info(
            _("Loading l10n_br_stock_account/demo/stock_inventory_demo.xml ...")
        )
        tools.convert_file(
            cr,
            "l10n_br_stock_account",
            "demo/stock_inventory_demo.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )

        # Load COA Fiscal Operation properties
        stock_account_inform_journal_in_fiscal_operation(cr)


def stock_account_inform_journal_in_fiscal_operation(cr):
    if not tools.config["without_demo"]:
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Load COA Fiscal Operation properties
        company = env.ref(
            "l10n_br_base.empresa_simples_nacional", raise_if_not_found=False
        )

        # COA Simple Fiscal Operation properties
        if company and env["ir.module.module"].search_count(
            [
                ("name", "=", "l10n_br_coa_simple"),
                ("state", "=", "installed"),
            ]
        ):
            # Load Fiscal Operation Main Company
            inform_journal_in_fiscal_operation(
                cr,
                env.ref("base.main_company"),
                [
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_entrada_remessa",
                        "journal": "l10n_br_stock_account."
                        "entrada_remessa_journal_main_company",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_simples_remessa",
                        "journal": "l10n_br_stock_account."
                        "simples_remessa_journal_main_company",
                    },
                ],
            )

            inform_journal_in_fiscal_operation(
                cr,
                company,
                [
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_entrada_remessa",
                        "journal": "l10n_br_stock_account."
                        "entrada_remessa_journal_simples_nacional",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_simples_remessa",
                        "journal": "l10n_br_stock_account."
                        "simples_remessa_journal_simples_nacional",
                    },
                ],
            )

        company_lc = env.ref(
            "l10n_br_base.empresa_lucro_presumido", raise_if_not_found=False
        )

        # COA Generic Fiscal Operation properties
        if company_lc and env["ir.module.module"].search_count(
            [
                ("name", "=", "l10n_br_coa_generic"),
                ("state", "=", "installed"),
            ]
        ):
            inform_journal_in_fiscal_operation(
                cr,
                company_lc,
                [
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_entrada_remessa",
                        "journal": "l10n_br_stock_account."
                        "entrada_remessa_journal_lucro_presumido",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_simples_remessa",
                        "journal": "l10n_br_stock_account."
                        "simples_remessa_journal_lucro_presumido",
                    },
                ],
            )
