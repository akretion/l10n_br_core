# Copyright (C) 2020  Renato Lima - Akretion <renato.lima@akretion.com.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging

from odoo import SUPERUSER_ID, _, api, tools

from odoo.addons.l10n_br_fiscal.tools import inform_journal_in_fiscal_operation

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    if not tools.config["without_demo"]:
        _logger.info(_("Loading l10n_br_sale/demo/product.xml ..."))
        tools.convert_file(
            cr,
            "l10n_br_sale",
            "demo/product.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )
        _logger.info(_("Loading l10n_br_sale/demo/company.xml ..."))
        tools.convert_file(
            cr,
            "l10n_br_sale",
            "demo/company.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )
        _logger.info(_("Loading l10n_br_sale/demo/l10n_br_sale.xml ..."))
        tools.convert_file(
            cr,
            "l10n_br_sale",
            "demo/l10n_br_sale.xml",
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )

        # Create or Inform Fiscal Operation in Journal for Property of Companies
        env = api.Environment(cr, SUPERUSER_ID, {})
        sale_orders = env["sale.order"].search(
            [("company_id", "!=", env.ref("base.main_company").id)]
        )

        for order in sale_orders:
            defaults = order.with_user(user=order.user_id.id).default_get(order._fields)
            defaults.update(
                {
                    "name": order.name,
                    "fiscal_operation_id": order.fiscal_operation_id.id,
                }
            )
            order.write(defaults)

        # Load COA Fiscal Operation properties
        sale_inform_journal_in_fiscal_operation(cr)


def sale_inform_journal_in_fiscal_operation(cr):
    if not tools.config["without_demo"]:
        # Create or Inform Fiscal Operation in Journal for Property of Companies
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
                        "fiscal_operation": "l10n_br_fiscal.fo_venda",
                        "journal": "l10n_br_coa_simple.sale_journal_main_company",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_bonificacao",
                        "journal": "l10n_br_coa_simple.general_journal_main_company",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_devolucao_venda",
                        "journal": "l10n_br_coa_simple.general_journal_main_company",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_simples_remessa",
                        "journal": "l10n_br_coa_simple.general_journal_main_company",
                    },
                ],
            )

            inform_journal_in_fiscal_operation(
                cr,
                company,
                [
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_venda",
                        "journal": "l10n_br_coa_simple.sale_journal_empresa_sn",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_bonificacao",
                        "journal": "l10n_br_coa_simple.general_journal_empresa_sn",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_devolucao_venda",
                        "journal": "l10n_br_coa_simple.general_journal_empresa_sn",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_simples_remessa",
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
            inform_journal_in_fiscal_operation(
                cr,
                company_lc,
                [
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_venda",
                        "journal": "l10n_br_coa_generic.sale_journal_empresa_lp",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_bonificacao",
                        "journal": "l10n_br_coa_generic.general_journal_empresa_lp",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_devolucao_venda",
                        "journal": "l10n_br_coa_generic.general_journal_empresa_lp",
                    },
                    {
                        "fiscal_operation": "l10n_br_fiscal.fo_simples_remessa",
                        "journal": "l10n_br_coa_generic.general_journal_empresa_lp",
                    },
                ],
            )
