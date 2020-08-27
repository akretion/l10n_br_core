# Copyright (C) 2009  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Brazilian - Simple Accounting",
    "summary": "Brazilian Simple Chart of Account",
    "category": "Localization",
    "license": "AGPL-3",
    "author": "Akretion, " "Odoo Community Association (OCA)",
    "website": "http://github.com/OCA/l10n-brazil",
    "version": "12.0.1.0.1",
    "depends": ["l10n_br_coa", "l10n_br_base"],
    "data": [
        "data/l10n_br_coa_simple_template.xml",
        "data/account_group.xml",
        "data/account.account.template.csv",
        "data/l10n_br_coa_simple_template_post.xml",
    ],
    "post_init_hook": "post_init_hook",
}
