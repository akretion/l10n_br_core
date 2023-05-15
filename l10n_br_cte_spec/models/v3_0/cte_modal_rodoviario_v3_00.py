# Copyright 2022 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/xsdata-odoo
#
import textwrap
from odoo import fields, models

from .tipos_geral_cte_v3_00 import TUF

__NAMESPACE__ = "http://www.portalfiscal.inf.br/cte"


class Rodo(models.AbstractModel):
    "Informações do modal Rodoviário"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "cte.30.rodo"
    _inherit = "spec.mixin.cte"
    _binding_type = "Rodo"

    cte30_RNTRC = fields.Char(
        string="Registro Nacional",
        xsd_required=True,
        help=(
            "Registro Nacional de Transportadores Rodoviários de "
            "Carga\nRegistro obrigatório do emitente do CT-e junto à ANTT para"
            " exercer a atividade de transportador rodoviário de cargas por "
            "conta de terceiros e mediante remuneração."
        ),
    )

    cte30_occ = fields.One2many(
        "cte.30.occ", "cte30_occ_rodo_id", string="Ordens de Coleta associados"
    )


class Occ(models.AbstractModel):
    "Ordens de Coleta associados"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "cte.30.occ"
    _inherit = "spec.mixin.cte"
    _binding_type = "Rodo.Occ"

    cte30_occ_rodo_id = fields.Many2one(
        comodel_name="cte.30.rodo", xsd_implicit=True, ondelete="cascade"
    )
    cte30_serie = fields.Char(string="Série da OCC")

    cte30_nOcc = fields.Char(string="Número da Ordem de coleta", xsd_required=True)

    cte30_dEmi = fields.Date(
        string="Data de emissão da ordem de coleta",
        xsd_required=True,
        xsd_type="TData",
        help="Data de emissão da ordem de coleta\nFormato AAAA-MM-DD",
    )

    cte30_emiOcc = fields.Many2one(
        comodel_name="cte.30.emiocc", string="emiOcc", xsd_required=True
    )


class EmiOcc(models.AbstractModel):
    _description = "emiOcc"
    _name = "cte.30.emiocc"
    _inherit = "spec.mixin.cte"
    _binding_type = "Rodo.Occ.EmiOcc"

    cte30_CNPJ = fields.Char(
        string="Número do CNPJ",
        xsd_required=True,
        xsd_type="TCnpj",
        help="Número do CNPJ\nInformar os zeros não significativos.",
    )

    cte30_cInt = fields.Char(
        string="Código interno de uso da transportadora",
        help=(
            "Código interno de uso da transportadora\nUso intermo das "
            "transportadoras."
        ),
    )

    cte30_IE = fields.Char(
        string="Inscrição Estadual", xsd_required=True, xsd_type="TIe"
    )

    cte30_UF = fields.Selection(
        TUF,
        string="Sigla da UF",
        xsd_required=True,
        xsd_type="TUf",
        help="Sigla da UF\nInformar EX para operações com o exterior.",
    )

    cte30_fone = fields.Char(string="Telefone", xsd_type="TFone")
