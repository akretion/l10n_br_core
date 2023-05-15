# Copyright 2022 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/xsdata-odoo
#
import textwrap
from odoo import fields, models

__NAMESPACE__ = "http://www.portalfiscal.inf.br/cte"

"Indicador Negociável"
MULTIMODAL_INDNEGOCIAVEL = [
    ("0", "Não Negociável"),
    ("1", "Negociável"),
]


class Multimodal(models.AbstractModel):
    "Informações do Multimodal"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "cte.30.multimodal"
    _inherit = "spec.mixin.cte"
    _binding_type = "Multimodal"

    cte30_COTM = fields.Char(
        string="Número do Certificado do Operador",
        xsd_required=True,
        help="Número do Certificado do Operador de Transporte Multimodal",
    )

    cte30_indNegociavel = fields.Selection(
        MULTIMODAL_INDNEGOCIAVEL,
        string="Indicador Negociável",
        xsd_required=True,
        help=(
            "Indicador Negociável\nPreencher com: 0 - Não Negociável; 1 - " "Negociável"
        ),
    )

    cte30_seg = fields.Many2one(
        comodel_name="cte.30.multimodal_seg",
        string="Informações de Seguro do Multimodal",
    )


class MultimodalSeg(models.AbstractModel):
    "Informações de Seguro do Multimodal"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "cte.30.multimodal_seg"
    _inherit = "spec.mixin.cte"
    _binding_type = "Multimodal.Seg"

    cte30_infSeg = fields.Many2one(
        comodel_name="cte.30.infseg",
        string="Informações da seguradora",
        xsd_required=True,
    )

    cte30_nApol = fields.Char(
        string="Número da Apólice",
        xsd_required=True,
        help="Número da Apólice\nObrigatório pela lei 11.442/07 (RCTRC)",
    )

    cte30_nAver = fields.Char(
        string="Número da Averbação",
        xsd_required=True,
        help=(
            "Número da Averbação\nNão é obrigatório, pois muitas averbações "
            "ocorrem aapós a emissão do CT, mensalmente, por exemplo."
        ),
    )


class InfSeg(models.AbstractModel):
    "Informações da seguradora"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "cte.30.infseg"
    _inherit = "spec.mixin.cte"
    _binding_type = "Multimodal.Seg.InfSeg"

    cte30_xSeg = fields.Char(string="Nome da Seguradora", xsd_required=True)

    cte30_CNPJ = fields.Char(
        string="Número do CNPJ da seguradora",
        xsd_required=True,
        xsd_type="TCnpjOpc",
        help=(
            "Número do CNPJ da seguradora\nObrigatório apenas se responsável "
            "pelo seguro for (2) responsável pela contratação do transporte - "
            "pessoa jurídica"
        ),
    )
