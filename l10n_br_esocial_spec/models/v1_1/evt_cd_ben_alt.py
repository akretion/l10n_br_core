# Copyright 2023 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/xsdata-odoo
#
import textwrap
from odoo import fields, models
from .tipos import (
    TSSIMNAO,
    TSTPPENMORTE,
    TSTPPLANRP,
    TIdeBeneficio,
    TIdeEmpregadorCnpj,
    TIdeEventoTrabPj,
)

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtCdBenAlt/v_S_01_01_00"

"Motivo da suspensão do benefício."
SUSPENSAO_MTVSUSPENSAO = [
    ("01", "Suspensão por não recadastramento"),
    ("99", "Outros motivos de suspensão"),
]


class ESocial(models.AbstractModel):
    "S-2416 - Cadastro de Benefício - Entes Públicos - Alteração"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.esocial"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial"

    eso11_evtCdBenAlt = fields.Many2one(
        comodel_name="eso.11.evtcdbenalt",
        string="Evento Cadastro de Benefício",
        xsd_required=True,
        help=(
            "Evento Cadastro de Benefício - "
            "Alteração\nDESCRICAO_COMPLETA:Evento Cadastro de Benefício - "
            "Entes Públicos - Alteração.\nCHAVE_GRUPO: {Id}\nREGRA:REGRA_ALTER"
            "A_TIPO_BENEFICIO\nREGRA:REGRA_BENEFICIO_ATIVO_NA_DTEVENTO\nREGRA:"
            "REGRA_ENVIO_PROC_FECHAMENTO\nREGRA:REGRA_EVENTOS_EXTEMP\nREGRA:RE"
            "GRA_EXISTE_INFO_EMPREGADOR\nREGRA:REGRA_EXTEMP_REATIVACAO\nREGRA:"
            "REGRA_RETIFICA_MESMO_BENEFICIO"
        ),
    )


class EvtCdBenAlt(models.AbstractModel):
    """Evento Cadastro de Benefício - Alteração
    DESCRICAO_COMPLETA:Evento Cadastro de Benefício - Entes Públicos - Alteração.
    CHAVE_GRUPO: {Id}
    REGRA:REGRA_ALTERA_TIPO_BENEFICIO
    REGRA:REGRA_BENEFICIO_ATIVO_NA_DTEVENTO
    REGRA:REGRA_ENVIO_PROC_FECHAMENTO
    REGRA:REGRA_EVENTOS_EXTEMP
    REGRA:REGRA_EXISTE_INFO_EMPREGADOR
    REGRA:REGRA_EXTEMP_REATIVACAO
    REGRA:REGRA_RETIFICA_MESMO_BENEFICIO"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.evtcdbenalt"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtCdBenAlt"

    eso11_ideEvento = fields.Many2one(
        comodel_name="eso.11.tideeventotrabpj",
        string="ideEvento",
        xsd_required=True,
        xsd_type="T_ideEvento_trab_PJ",
    )

    eso11_ideEmpregador = fields.Many2one(
        comodel_name="eso.11.tideempregadorcnpj",
        string="ideEmpregador",
        xsd_required=True,
        xsd_type="T_ideEmpregador_cnpj",
    )

    eso11_ideBeneficio = fields.Many2one(
        comodel_name="eso.11.tidebeneficio",
        string="ideBeneficio",
        xsd_required=True,
        xsd_type="T_ideBeneficio",
    )

    eso11_infoBenAlteracao = fields.Many2one(
        comodel_name="eso.11.infobenalteracao",
        string="Informações do benefício",
        xsd_required=True,
        help=(
            "Informações do benefício - Alteração.\nCHAVE_GRUPO: " "{dtAltBeneficio*}"
        ),
    )

    eso11_Id = fields.Char(string="Id", xsd_required=True, xsd_type="TS_Id")


class InfoBenAlteracao(models.AbstractModel):
    """Informações do benefício - Alteração.
    CHAVE_GRUPO: {dtAltBeneficio*}"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.infobenalteracao"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtCdBenAlt.InfoBenAlteracao"

    eso11_dtAltBeneficio = fields.Date(
        string="Data de alteração",
        xsd_required=True,
        xsd_type="xs:date",
        help=(
            "Data de alteração das informações relativas ao "
            "benefício.\nValidação: Deve ser igual ou anterior à data atual."
        ),
    )

    eso11_dadosBeneficio = fields.Many2one(
        comodel_name="eso.11.dadosbeneficio",
        string="Dados relativos ao benefício",
        xsd_required=True,
    )


class DadosBeneficio(models.AbstractModel):
    "Dados relativos ao benefício."
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.dadosbeneficio"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtCdBenAlt.InfoBenAlteracao.DadosBeneficio"

    eso11_tpBeneficio = fields.Char(
        string="Tipo de benefício",
        xsd_required=True,
        xsd_type="TS_tpBeneficio",
        help=(
            "Tipo de benefício.\nValidação: Deve ser um código válido e "
            "existente na Tabela 25. Se {cadIni}(2410_infoBenInicio_cadIni) em"
            " S-2410 for igual a [N], não é permitido utilizar código do grupo"
            " [08] dessa tabela."
        ),
    )

    eso11_tpPlanRP = fields.Selection(
        TS_TPPLANRP, string="tpPlanRP", xsd_required=True, xsd_type="TS_tpPlanRP"
    )

    eso11_dsc = fields.Char(
        string="Descrição do instrumento ou situação",
        xsd_type="TS_texto_255",
        help=(
            "Descrição do instrumento ou situação que originou o pagamento do "
            "benefício.\nValidação: Preenchimento obrigatório se "
            "{tpBeneficio}(./tpBeneficio) = [0909, 1001, 1009]."
        ),
    )

    eso11_indSuspensao = fields.Selection(
        TS_SIM_NAO,
        string="Indicativo de suspensão do benefício",
        xsd_required=True,
        xsd_type="TS_sim_nao",
    )

    eso11_infoPenMorte = fields.Many2one(
        comodel_name="eso.11.infopenmorte",
        string="Informações relativas à pensão por morte",
        help=(
            "Informações relativas à pensão por morte.\nCONDICAO_GRUPO: O (se "
            "{tpBeneficio}(../tpBeneficio) pertencer ao grupo [06]); N (nos "
            "demais casos)"
        ),
    )

    eso11_suspensao = fields.Many2one(
        comodel_name="eso.11.suspensao",
        string="Informações referentes à suspensão",
        help=(
            "Informações referentes à suspensão do benefício.\nCONDICAO_GRUPO:"
            " O (se {indSuspensao}(../indSuspensao) = [S]; N (se "
            "{indSuspensao}(../indSuspensao) = [N]"
        ),
    )


class InfoPenMorte(models.AbstractModel):
    """Informações relativas à pensão por morte.
    CONDICAO_GRUPO: O (se {tpBeneficio}(../tpBeneficio) pertencer ao grupo [06]); N
    (nos demais casos)"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.infopenmorte"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtCdBenAlt.InfoBenAlteracao.DadosBeneficio.InfoPenMorte"

    eso11_tpPenMorte = fields.Selection(
        TS_TPPENMORTE, string="tpPenMorte", xsd_required=True, xsd_type="TS_tpPenMorte"
    )


class Suspensao(models.AbstractModel):
    """Informações referentes à suspensão do benefício.
    CONDICAO_GRUPO: O (se {indSuspensao}(../indSuspensao) = [S]; N (se
    {indSuspensao}(../indSuspensao) = [N]"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.suspensao"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtCdBenAlt.InfoBenAlteracao.DadosBeneficio.Suspensao"

    eso11_mtvSuspensao = fields.Selection(
        SUSPENSAO_MTVSUSPENSAO, string="mtvSuspensao", xsd_required=True
    )

    eso11_dscSuspensao = fields.Char(
        string="Descrição do motivo da suspensão",
        xsd_type="TS_texto_255",
        help=(
            "Descrição do motivo da suspensão do benefício.\nValidação: "
            "Preenchimento obrigatório e exclusivo se "
            "{mtvSuspensao}(./mtvSuspensao) = [99]."
        ),
    )
