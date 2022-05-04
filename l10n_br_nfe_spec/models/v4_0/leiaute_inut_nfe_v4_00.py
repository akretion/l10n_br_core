# Copyright 2022 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/xsdata-odoo
#
import textwrap
from odoo import fields, models
from .tipos_basico_v4_00 import (
    TAMB,
    TCODUFIBGE,
    TMOD,
)

__NAMESPACE__ = "http://www.portalfiscal.inf.br/nfe"

"Serviço Solicitado"
INFINUT_XSERV = [
    ("INUTILIZAR", "INUTILIZAR"),
]


class TinutNfe(models.AbstractModel):
    "Tipo Pedido de Inutilização de Numeração da Nota Fiscal Eletrônica"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "nfe.40.tinutnfe"
    _inherit = "spec.mixin.nfe"
    _binding_type = "TinutNfe"

    nfe40_infInut = fields.Many2one(
        comodel_name="nfe.40.infinut",
        string="Dados do Pedido de Inutilização",
        xsd_required=True,
        help=(
            "Dados do Pedido de Inutilização de Numeração da Nota Fiscal " "Eletrônica"
        ),
    )

    nfe40_versao = fields.Char(
        string="versao", xsd_required=True, xsd_type="TVerInutNFe"
    )


class InfInut(models.AbstractModel):
    """Dados do Pedido de Inutilização de Numeração da Nota Fiscal
    Eletrônica"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "nfe.40.infinut"
    _inherit = "spec.mixin.nfe"
    _binding_type = "TinutNfe.InfInut"

    nfe40_tpAmb = fields.Selection(
        TAMB,
        string="Identificação do Ambiente",
        xsd_required=True,
        xsd_type="TAmb",
        help="Identificação do Ambiente:\n1 - Produção\n2 - Homologação",
    )

    nfe40_xServ = fields.Selection(
        INFINUT_XSERV, string="Serviço Solicitado", xsd_required=True
    )

    nfe40_cUF = fields.Selection(
        TCODUFIBGE,
        string="Código da UF do emitente",
        xsd_required=True,
        xsd_type="TCodUfIBGE",
    )

    nfe40_ano = fields.Char(
        string="Ano de inutilização da numeração", xsd_required=True, xsd_type="Tano"
    )

    nfe40_CNPJ = fields.Char(
        string="CNPJ do emitente", xsd_required=True, xsd_type="TCnpj"
    )

    nfe40_mod = fields.Selection(
        TMOD, string="Modelo da NF-e (55, 65 etc.)", xsd_required=True, xsd_type="TMod"
    )

    nfe40_serie = fields.Char(
        string="Série da NF-e", xsd_required=True, xsd_type="TSerie"
    )

    nfe40_nNFIni = fields.Char(
        string="Número da NF-e inicial", xsd_required=True, xsd_type="TNF"
    )

    nfe40_nNFFin = fields.Char(
        string="Número da NF-e final", xsd_required=True, xsd_type="TNF"
    )

    nfe40_xJust = fields.Char(
        string="Justificativa do pedido de inutilização",
        xsd_required=True,
        xsd_type="TJust",
    )

    nfe40_Id = fields.Char(string="Id", xsd_required=True)


class TretInutNfe(models.AbstractModel):
    """Tipo retorno do Pedido de Inutilização de Numeração da Nota Fiscal
    Eletrônica"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "nfe.40.tretinutnfe"
    _inherit = "spec.mixin.nfe"
    _binding_type = "TretInutNfe"

    nfe40_infInut = fields.Many2one(
        comodel_name="nfe.40.infinut",
        string="Dados do Retorno do Pedido",
        xsd_required=True,
        help=(
            "Dados do Retorno do Pedido de Inutilização de Numeração da Nota "
            "Fiscal Eletrônica"
        ),
    )

    nfe40_versao = fields.Char(
        string="versao", xsd_required=True, xsd_type="TVerInutNFe"
    )


class InfInut(models.AbstractModel):
    """Dados do Pedido de Inutilização de Numeração da Nota Fiscal
    Eletrônica"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "nfe.40.infinut"
    _inherit = "spec.mixin.nfe"
    _binding_type = "TretInutNfe.InfInut"

    nfe40_tpAmb = fields.Selection(
        TAMB,
        string="Identificação do Ambiente",
        xsd_required=True,
        xsd_type="TAmb",
        help="Identificação do Ambiente:\n1 - Produção\n2 - Homologação",
    )

    nfe40_verAplic = fields.Char(
        string="Versão do Aplicativo que processou",
        xsd_required=True,
        xsd_type="TVerAplic",
        help="Versão do Aplicativo que processou a NF-e",
    )

    nfe40_cStat = fields.Char(
        string="Código do status da mensagem enviada",
        xsd_required=True,
        xsd_type="TStat",
    )

    nfe40_xMotivo = fields.Char(
        string="Descrição literal do status",
        xsd_required=True,
        xsd_type="TMotivo",
        help="Descrição literal do status do serviço solicitado.",
    )

    nfe40_cUF = fields.Selection(
        TCODUFIBGE,
        string="Código da UF que atendeu a solicitação",
        xsd_required=True,
        xsd_type="TCodUfIBGE",
    )

    nfe40_ano = fields.Char(string="Ano de inutilização da numeração", xsd_type="Tano")

    nfe40_CNPJ = fields.Char(string="CNPJ do emitente", xsd_type="TCnpj")

    nfe40_mod = fields.Selection(
        TMOD, string="Modelo da NF-e (55, etc.)", xsd_type="TMod"
    )

    nfe40_serie = fields.Char(string="Série da NF-e", xsd_type="TSerie")

    nfe40_nNFIni = fields.Char(string="Número da NF-e inicial", xsd_type="TNF")

    nfe40_nNFFin = fields.Char(string="Número da NF-e final", xsd_type="TNF")

    nfe40_dhRecbto = fields.Datetime(
        string="Data e hora de recebimento",
        xsd_required=True,
        xsd_type="TDateTimeUTC",
        help=(
            "Data e hora de recebimento, no formato AAAA-MM-DDTHH:MM:SS. Deve "
            "ser preenchida com data e hora da gravação no Banco em caso de "
            "Confirmação. Em caso de Rejeição, com data e hora do recebimento "
            "do Pedido de Inutilização."
        ),
    )

    nfe40_nProt = fields.Char(
        string="Número do Protocolo de Status da NF-e",
        xsd_type="TProt",
        help=(
            "Número do Protocolo de Status da NF-e. 1 posição (1 – Secretaria "
            "de Fazenda Estadual 2 – Receita Federal); 2 - código da UF - 2 "
            "posições ano; 10 seqüencial no ano."
        ),
    )

    nfe40_Id = fields.Char(string="Id")


class TprocInutNfe(models.AbstractModel):
    "Tipo Pedido de inutilzação de númeração de NF-e processado"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "nfe.40.tprocinutnfe"
    _inherit = "spec.mixin.nfe"
    _binding_type = "TprocInutNfe"

    nfe40_inutNFe = fields.Many2one(
        comodel_name="nfe.40.tinutnfe",
        string="inutNFe",
        xsd_required=True,
        xsd_type="TInutNFe",
    )

    nfe40_retInutNFe = fields.Many2one(
        comodel_name="nfe.40.tretinutnfe",
        string="retInutNFe",
        xsd_required=True,
        xsd_type="TRetInutNFe",
    )

    nfe40_versao = fields.Char(
        string="versao", xsd_required=True, xsd_type="TVerInutNFe"
    )
