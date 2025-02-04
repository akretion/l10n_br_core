# Copyright (C) 2020  Renato Lima - Akretion <renato.lima@akretion.com.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging

from odoo import SUPERUSER_ID, _, api, tools

from odoo.addons.l10n_br_fiscal.tools import inform_journal_in_fiscal_operation

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    if not tools.config["without_demo"]:
        _logger.info(_("Loading l10n_br_purchase/demo/company.xml ..."))
        tools.convert_file(
            cr,
            "l10n_br_purchase",
            "demo/company.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )
        _logger.info(_("Loading l10n_br_purchase/demo/product.xml ..."))
        tools.convert_file(
            cr,
            "l10n_br_purchase",
            "demo/product.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )
        _logger.info(_("Loading l10n_br_purchase/demo/l10n_br_purchase.xml ..."))
        tools.convert_file(
            cr,
            "l10n_br_purchase",
            "demo/l10n_br_purchase.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )

        env = api.Environment(cr, SUPERUSER_ID, {})
        purchase_orders = env["purchase.order"].search(
            [("company_id", "!=", env.ref("base.main_company").id)]
        )

        for order in purchase_orders:
            defaults = order.with_context(company_id=order.company_id.id).default_get(
                order._fields
            )
            defaults.update(
                {
                    "name": order.name,
                    "company_id": order.company_id.id,
                    "fiscal_operation_id": order.fiscal_operation_id.id,
                }
            )
            order.write(defaults)

        # Load COA Fiscal Operation properties
        purchase_inform_journal_in_fiscal_operation(cr)


def purchase_inform_journal_in_fiscal_operation(cr):
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
                        "fiscal_operation": "l10n_br_fiscal.fo_compras",
                        "journal": "l10n_br_coa_simple.purchase_journal_main_company",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_devolucao_compras",
                        "journal": "l10n_br_coa_simple.general_journal_main_company",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_entrada_remessa",
                        "journal": "l10n_br_coa_simple.general_journal_main_company",
                    },
                ],
            )

            # Load Fiscal Operation for Simples Nacional
            inform_journal_in_fiscal_operation(
                cr,
                company,
                [
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_compras",
                        "journal": "l10n_br_coa_simple.purchase_journal_empresa_sn",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_devolucao_compras",
                        "journal": "l10n_br_coa_simple.general_journal_empresa_sn",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_entrada_remessa",
                        "journal": "l10n_br_coa_simple.general_journal_empresa_sn",
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
            # Load Fiscal Operation for Lucro Presumido
            inform_journal_in_fiscal_operation(
                cr,
                company_lc,
                [
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_compras",
                        "journal": "l10n_br_coa_generic.purchase_journal_empresa_lp",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_devolucao_compras",
                        "journal": "l10n_br_coa_generic.general_journal_empresa_lp",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_entrada_remessa",
                        "journal": "l10n_br_coa_generic.general_journal_empresa_lp",
                    },
                ],
            )
