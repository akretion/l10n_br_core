# Copyright 2023 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/xsdata-odoo
#
import textwrap
from odoo import fields, models
from .tipos import (
    TIdeEmpregador,
    TIdeEventoFolhaMensal,
)

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtPgtos/v_S_01_01_00"

"Indicativo do Número de Identificação Fiscal (NIF)."
INFOPGTOEXT_INDNIF = [
  ("1", "Beneficiário com NIF"),
  ("2", "Beneficiário dispensado do NIF"),
  ("3", "País não exige NIF"),
]

"Informar o evento de origem do pagamento."
INFOPGTO_TPPGTO = [
  ("1", "Pagamento de remuneração, conforme apurado em {ideDmDev}(1200_dmDev_ideDmDev) do S-1200"),
  ("2", "Pagamento de verbas rescisórias conforme apurado em {ideDmDev}(2299_infoDeslig_verbasResc_dmDev_ideDmDev) do S-2299"),
  ("3", "Pagamento de verbas rescisórias conforme apurado em {ideDmDev}(2399_infoTSVTermino_verbasResc_dmDev_ideDmDev) do S-2399"),
  ("4", "Pagamento de remuneração conforme apurado em {ideDmDev}(1202_dmDev_ideDmDev) do S-1202"),
  ("5", "Pagamento de benefícios previdenciários, conforme apurado em {ideDmDev}(1207_dmDev_ideDmDev) do S-1207"),
]


class ESocial(models.AbstractModel):
    "S-1210 - Pagamentos de Rendimentos do Trabalho"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.esocial"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial"


    
    eso11_evtPgtos = fields.Many2one(
        comodel_name="eso.11.evtpgtos",
        string="Evento Pagamentos de Rendimentos",
        xsd_required=True,
        help=(
            "Evento Pagamentos de Rendimentos do Trabalho.\nCHAVE_GRUPO: {Id}\"
            "nREGRA:REGRA_CONTROLE_DUPLICIDADE\nREGRA:REGRA_EMPREGADO_DOMESTIC"
            "O\nREGRA:REGRA_ENVIO_PROC_FECHAMENTO\nREGRA:REGRA_EVENTOS_EXTEMP\"
            "nREGRA:REGRA_EVE_FOPAG_SIMPLIFICADO\nREGRA:REGRA_EXISTE_INFO_EMPR"
            "EGADOR\nREGRA:REGRA_MESMO_PROCEMI\nREGRA:REGRA_PAGTO_IND_RETIFICA"
            "CAO\nREGRA:REGRA_PAGTO_PERMITE_EXCLUSAO\nREGRA:REGRA_VALIDA_DT_PG"
            "TO\nREGRA:REGRA_VALIDA_EMPREGADOR\nREGRA:REGRA_VALIDA_PER_APUR_PG"
            "TO"
        )
    )
    

class EvtPgtos(models.AbstractModel):
    """Evento Pagamentos de Rendimentos do Trabalho.
    CHAVE_GRUPO: {Id}
    REGRA:REGRA_CONTROLE_DUPLICIDADE
    REGRA:REGRA_EMPREGADO_DOMESTICO
    REGRA:REGRA_ENVIO_PROC_FECHAMENTO
    REGRA:REGRA_EVENTOS_EXTEMP
    REGRA:REGRA_EVE_FOPAG_SIMPLIFICADO
    REGRA:REGRA_EXISTE_INFO_EMPREGADOR
    REGRA:REGRA_MESMO_PROCEMI
    REGRA:REGRA_PAGTO_IND_RETIFICACAO
    REGRA:REGRA_PAGTO_PERMITE_EXCLUSAO
    REGRA:REGRA_VALIDA_DT_PGTO
    REGRA:REGRA_VALIDA_EMPREGADOR
    REGRA:REGRA_VALIDA_PER_APUR_PGTO"""
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.evtpgtos"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtPgtos"


    
    eso11_ideEvento = fields.Many2one(
        comodel_name="eso.11.tideeventofolhamensal",
        string="ideEvento",
        xsd_required=True,
        xsd_type="T_ideEvento_folha_mensal"
    )
    
    eso11_ideEmpregador = fields.Many2one(
        comodel_name="eso.11.tideempregador",
        string="ideEmpregador",
        xsd_required=True,
        xsd_type="T_ideEmpregador"
    )
    
    eso11_ideBenef = fields.Many2one(
        comodel_name="eso.11.idebenef",
        string="Identificação do beneficiário",
        xsd_required=True,
        help=(
            "Identificação do beneficiário do pagamento.\nCHAVE_GRUPO: "
            "{cpfBenef*}"
        )
    )
    
    eso11_Id = fields.Char(
        string="Id",
        xsd_required=True,
        xsd_type="TS_Id"
    )
    

class IdeBenef(models.AbstractModel):
    """Identificação do beneficiário do pagamento.
    CHAVE_GRUPO: {cpfBenef*}"""
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.idebenef"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtPgtos.IdeBenef"


    
    eso11_cpfBenef = fields.Char(
        string="CPF do beneficiário",
        xsd_required=True,
        xsd_type="TS_cpf",
        help=(
            "CPF do beneficiário.\nValidação: Deve ser o mesmo CPF informado "
            "no evento de remuneração ou desligamento (S-1200, S-1202, S-1207,"
            " S-2299 ou S-2399)."
        )
    )
    
    eso11_infoPgto = fields.One2many("eso.11.infopgto", "eso11_infoPgto_ideBenef_id",
        string="Informações dos pagamentos efetuados",
        help=(
            "Informações dos pagamentos efetuados.\nCHAVE_GRUPO: {tpPgto}, "
            "{perRef}, {ideDmDev}"
        )
    )
    

class InfoPgto(models.AbstractModel):
    """Informações dos pagamentos efetuados.
    CHAVE_GRUPO: {tpPgto}, {perRef}, {ideDmDev}"""
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.infopgto"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtPgtos.IdeBenef.InfoPgto"


    
    eso11_dtPgto = fields.Date(
        string="data de pagamento",
        xsd_required=True,
        xsd_type="xs:date",
        help=(
            "data de pagamento.\nValidação: A data informada deve estar "
            "compreendida no período de apuração "
            "({perApur}(1210_ideEvento_perApur)), exceto se "
            "{procEmi}(1210_ideEvento_procEmi) = [2, 4, 22]."
        )
    )
    
    eso11_tpPgto = fields.Selection(INFOPGTO_TPPGTO,
        string="tpPgto",
        xsd_required=True
    )
    
    eso11_perRef = fields.Char(
        string="competência declarada no campo {perApur}",
        xsd_required=True,
        xsd_type="TS_perApur",
        help=(
            "competência declarada no campo {perApur} do evento remuneratório "
            "a que se refere o pagamento, no formato AAAA-MM (ou AAAA, se for "
            "relativa à folha de 13° salário). Se "
            "{tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [2, 3], informar o "
            "mês/ano da data de desligamento (ou de término), no formato AAAA-"
            "MM.\nValidação: Deve corresponder ao conteúdo indicado na relação"
            " a seguir:\nSe {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [1], "
            "{perApur}(1200_ideEvento_perApur) do S-1200;\nSe "
            "{tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [2], mês/ano de "
            "{dtDeslig}(2299_infoDeslig_dtDeslig) do S-2299 (formato AAAA-"
            "MM);\nSe {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [3], mês/ano "
            "de {dtTerm}(2399_infoTSVTermino_dtTerm) do S-2399 (formato AAAA-"
            "MM);\nSe {tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [4], "
            "{perApur}(1202_ideEvento_perApur) do S-1202;\nSe "
            "{tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [5], "
            "{perApur}(1207_ideEvento_perApur) do S-1207."
        )
    )
    
    eso11_ideDmDev = fields.Char(
        string="Identificador atribuído",
        xsd_required=True,
        xsd_type="TS_codigo_esocial",
        help=(
            "Identificador atribuído pela fonte pagadora para o demonstrativo "
            "de valores devidos ao trabalhador conforme definido em S-1200, "
            "S-1202, S-1207, S-2299 ou S-2399.\nValidação: Deve ser um valor "
            "atribuído pela fonte pagadora em S-1200, S-1202, S-1207, S-2299 "
            "ou S-2399 no campo {ideDmDev}, obedecendo à relação:\nSe "
            "{tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [1], em S-1200;\nSe "
            "{tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [2], em S-2299;\nSe "
            "{tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [3], em S-2399;\nSe "
            "{tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [4], em S-1202;\nSe "
            "{tpPgto}(1210_ideBenef_infoPgto_tpPgto) = [5], em S-1207."
        )
    )
    
    eso11_vrLiq = fields.Float(
        string="Valor líquido recebido pelo trabalhador",
        xsd_required=True,
        xsd_type="TS_valorMonetario",
        help=(
            "Valor líquido recebido pelo trabalhador, composto pelos "
            "vencimentos e descontos, inclusive os descontos de IRRF e de "
            "pensão alimentícia (se houver).\nValidação: Não pode ser um valor"
            " negativo."
        )
    )
    
    eso11_paisResidExt = fields.Char(
        string="código do país de residência",
        xsd_type="TS_pais",
        help=(
            "código do país de residência para fins fiscais, quando no "
            "exterior, conforme Tabela 06.\nSomente informar este campo caso o"
            " país de residência para fins fiscais seja diferente de Brasil. "
            "Se não informado, implica que o país de residência fiscal é "
            "Brasil.\nValidação: O campo apenas pode ser preenchido se "
            "{perApur}(1210_ideEvento_perApur) &gt;= [2023-03]. Se informado, "
            "deve ser um código válido e existente na Tabela 06, exceto [105]."
        )
    )
    
    eso11_infoPgtoExt = fields.Many2one(
        comodel_name="eso.11.infopgtoext",
        string="Informações complementares relativas",
        help=(
            "Informações complementares relativas a pagamentos a residente "
            "fiscal no exterior.\nCONDICAO_GRUPO: O (se "
            "{paisResidExt}(../paisResidExt) for informado); N (nos demais "
            "casos)"
        )
    )
    

class InfoPgtoExt(models.AbstractModel):
    """Informações complementares relativas a pagamentos a residente fiscal no
    exterior.
    CONDICAO_GRUPO: O (se {paisResidExt}(../paisResidExt) for informado); N (nos
    demais casos)"""
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.infopgtoext"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtPgtos.IdeBenef.InfoPgto.InfoPgtoExt"


    
    eso11_indNIF = fields.Selection(INFOPGTOEXT_INDNIF,
        string="indNIF",
        xsd_required=True
    )
    
    eso11_nifBenef = fields.Char(
        string="Número de Identificação Fiscal",
        xsd_type="TS_codigo_esocial",
        help=(
            "Número de Identificação Fiscal (NIF).\nValidação: Preenchimento "
            "obrigatório se {indNIF}(./indNIF) = [1]."
        )
    )
    
    eso11_frmTribut = fields.Char(
        string="frmTribut",
        xsd_required=True
    )
    
    eso11_endExt = fields.Many2one(
        comodel_name="eso.11.endext",
        string="Endereço do beneficiário residente",
        help=(
            "Endereço do beneficiário residente ou domiciliado no "
            "exterior.\nCONDICAO_GRUPO: OC\nREGRA:REGRA_ENDERECO_EXTERIOR"
        )
    )
    

class EndExt(models.AbstractModel):
    """Endereço do beneficiário residente ou domiciliado no exterior.
    CONDICAO_GRUPO: OC
    REGRA:REGRA_ENDERECO_EXTERIOR"""
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.endext"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtPgtos.IdeBenef.InfoPgto.InfoPgtoExt.EndExt"


    
    eso11_endDscLograd = fields.Char(
        string="endDscLograd"
    )
    
    eso11_endNrLograd = fields.Char(
        string="Número do logradouro",
        xsd_type="TS_nrLograd",
        help=(
            "Número do logradouro.\nValidação: Devem ser utilizados apenas "
            "caracteres alfanuméricos com, pelo menos, um caractere numérico."
        )
    )
    
    eso11_endComplem = fields.Char(
        string="endComplem",
        xsd_type="TS_complemento"
    )
    
    eso11_endBairro = fields.Char(
        string="endBairro"
    )
    
    eso11_endCidade = fields.Char(
        string="endCidade"
    )
    
    eso11_endEstado = fields.Char(
        string="endEstado"
    )
    
    eso11_endCodPostal = fields.Char(
        string="endCodPostal"
    )
    
    eso11_telef = fields.Char(
        string="telef"
    )