# Copyright (C) 2019 - Raphaël Valyi Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import SUPERUSER_ID, api
from odoo.tools.sql import column_exists, create_column


def pre_init_hook(cr):
    """
    account.invoice and account.invoice.line inherits from
    l10n_br_account.fiscal_document and l10n_br_account.fiscal_document.line
    respectively.
    But the problem is that you may have existing invoice and lines (like demo
    data or because you were using Odoo before installing this module or because
    you use your Odoo instance for other countries than Brazil) so we should
    make the Odoo ORM happy for these records and we do that with dummy records
    that we use to fill these new foreign keys.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    if not column_exists(cr, "account_invoice", "fiscal_document_id"):
        create_column(cr, "account_invoice", "fiscal_document_id", "INTEGER")
    fiscal_doc_id = env.ref("l10n_br_fiscal.fiscal_document_dummy").id
    cr.execute(
        """update account_invoice set fiscal_document_id=%s
               where fiscal_document_id IS NULL;""",
        (fiscal_doc_id,),
    )
    fiscal_doc_line_id = env.ref("l10n_br_fiscal.fiscal_document_line_dummy").id
    if not column_exists(cr, "account_invoice_line", "fiscal_document_line_id"):
        create_column(cr, "account_invoice_line", "fiscal_document_line_id", "INTEGER")
    cr.execute(
        """update account_invoice_line set fiscal_document_line_id=%s
               where fiscal_document_line_id IS NULL;""",
        (fiscal_doc_line_id,),
    )


def post_init_hook(cr, registry):
    """Relate fiscal taxes to account taxes."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    l10n_br_chart = env.ref("l10n_br_simple.l10n_br_account_chart_template")
    companies = env["res.company"].search(
        [("chart_template_id", "=", l10n_br_chart.id)]
    )

    for company in companies:
        taxes = env["account.tax"].search([("company_id", "=", company.id)])

        for tax in taxes:
            if tax.get_external_id():
                tax_ref = tax.get_external_id().get(tax.id)
                ref_module, ref_name = tax_ref.split(".")
                ref_name = ref_name.replace(str(company.id) + "_", "")
                tax_source_ref = ".".join([ref_module, ref_name])
                tax_template = env.ref(tax_source_ref)
                tax.fiscal_tax_id = tax_template.fiscal_tax_id
