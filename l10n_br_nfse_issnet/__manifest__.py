# Copyright 2020 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Edoc Nfse ISSNet',
    'summary': """
        NFS-e (ISSNet)""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-brazil',
    'external_dependencies': {
        'python': [
            'erpbrasil.edoc',
            'erpbrasil.assinatura',
            'erpbrasil.transmissao',
            'erpbrasil.base',
            'nfselib.issnet',
        ],
    },
    'depends': [
        'l10n_br_nfse',
    ],
    'demo': [
        'demo/city_taxation_code_demo.xml',
    ],
}
