# Copyright 2023 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/xsdata-odoo
#
import textwrap
from odoo import fields, models
from .tipos import (
    TSSIMNAO,
    TSTPINSC134,
    TSUF,
    TIdeEmpregador,
    TIdeEventoTrab,
    TIdeVinculoSst,
)

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtExpRisco/v_S_01_01_00"

"""Tipo de avaliação do agente nocivo.
    Validação: Preenchimento obrigatório e exclusivo se {codAgNoc}(./codAgNoc) for
    diferente de [09.01.001]."""
AGNOC_TPAVAL = [
    ("1", "Critério quantitativo"),
    ("2", "Critério qualitativo"),
]

"""Dose ou unidade de medida da intensidade ou concentração do agente.
    Validação: Preenchimento obrigatório e exclusivo se {tpAval}(./tpAval) =
    [1]."""
AGNOC_UNMED = [
    ("1", "dose diária de ruído"),
    ("2", "decibel linear (dB (linear))"),
    ("3", "decibel (C) (dB(C))"),
    ("4", "decibel (A) (dB(A))"),
    ("5", "metro por segundo ao quadrado (m/s^^2^^)"),
    ("6", "metro por segundo elevado a 1,75 (m/s^^1,75^^)"),
    ("7", "parte de vapor ou gás por milhão de partes de ar contaminado (ppm)"),
    ("8", "miligrama por metro cúbico de ar (mg/m^^3^^)"),
    ("9", "fibra por centímetro cúbico (f/cm^^3^^)"),
    ("10", "grau Celsius (ºC)"),
    ("11", "metro por segundo (m/s)"),
    ("12", "porcentual"),
    ("13", "lux (lx)"),
    ("14", "unidade formadora de colônias por metro cúbico (ufc/m^^3^^)"),
    ("15", "dose diária"),
    ("16", "dose mensal"),
    ("17", "dose trimestral"),
    ("18", "dose anual"),
    ("19", "watt por metro quadrado (W/m^^2^^)"),
    ("20", "ampère por metro (A/m)"),
    ("21", "militesla (mT)"),
    ("22", "microtesla (μT)"),
    ("23", "miliampère (mA)"),
    ("24", "quilovolt por metro (kV/m)"),
    ("25", "volt por metro (V/m)"),
    ("26", "joule por metro quadrado (J/m^^2^^)"),
    ("27", "milijoule por centímetro quadrado (mJ/cm^^2^^)"),
    ("28", "milisievert (mSv)"),
    ("29", "milhão de partículas por decímetro cúbico (mppdc)"),
    ("30", "umidade relativa do ar (UR (%))"),
]

"""O empregador implementa medidas de proteção coletiva (EPC) para eliminar
    ou reduzir a exposição dos trabalhadores ao agente nocivo?"""
EPCEPI_UTILIZEPC = [
    ("0", "Não se aplica"),
    ("1", "Não implementa"),
    ("2", "Implementa"),
]

"Utilização de EPI."
EPCEPI_UTILIZEPI = [
    ("0", "Não se aplica"),
    ("1", "Não utilizado"),
    ("2", "Utilizado"),
]

"Informar o tipo de estabelecimento do ambiente de trabalho."
INFOAMB_LOCALAMB = [
    ("1", "Estabelecimento do próprio empregador"),
    ("2", "Estabelecimento de terceiros"),
]

"""Órgão de classe ao qual o responsável pelos registros ambientais está
    vinculado.
    Validação: Preenchimento obrigatório se {codAgNoc}(../agNoc_codAgNoc) for
    diferente de [09.01.001]."""
RESPREG_IDEOC = [
    ("1", "Conselho Regional de Medicina - CRM"),
    ("4", "Conselho Regional de Engenharia e Agronomia - CREA"),
    ("9", "Outros"),
]


class ESocial(models.AbstractModel):
    "S-2240 - Condições Ambientais do Trabalho - Agentes Nocivos"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.esocial"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial"

    eso11_evtExpRisco = fields.Many2one(
        comodel_name="eso.11.evtexprisco",
        string="Evento Condições Ambientais do Trabalho",
        xsd_required=True,
        help=(
            "Evento Condições Ambientais do Trabalho - Agentes "
            "Nocivos.\nCHAVE_GRUPO: {Id}\nREGRA:REGRA_ENVIO_PROC_FECHAMENTO\nR"
            "EGRA:REGRA_EVENTOS_EXTEMP\nREGRA:REGRA_EVENTO_EXT_SEM_IMPACTO_FOP"
            "AG\nREGRA:REGRA_EVENTO_POSTERIOR_CAT_OBITO\nREGRA:REGRA_EXISTE_IN"
            "FO_EMPREGADOR\nREGRA:REGRA_EXTEMP_REINTEGRACAO\nREGRA:REGRA_GERAL"
            "_VALIDA_DADOS_TABCONTRIB\nREGRA:REGRA_MESMO_PROCEMI\nREGRA:REGRA_"
            "RETIFICA_MESMO_VINCULO\nREGRA:REGRA_TSV_ATIVO_NA_DTEVENTO\nREGRA:"
            "REGRA_VINCULO_ATIVO_NA_DTEVENTO"
        ),
    )


class EvtExpRisco(models.AbstractModel):
    """Evento Condições Ambientais do Trabalho - Agentes Nocivos.
    CHAVE_GRUPO: {Id}
    REGRA:REGRA_ENVIO_PROC_FECHAMENTO
    REGRA:REGRA_EVENTOS_EXTEMP
    REGRA:REGRA_EVENTO_EXT_SEM_IMPACTO_FOPAG
    REGRA:REGRA_EVENTO_POSTERIOR_CAT_OBITO
    REGRA:REGRA_EXISTE_INFO_EMPREGADOR
    REGRA:REGRA_EXTEMP_REINTEGRACAO
    REGRA:REGRA_GERAL_VALIDA_DADOS_TABCONTRIB
    REGRA:REGRA_MESMO_PROCEMI
    REGRA:REGRA_RETIFICA_MESMO_VINCULO
    REGRA:REGRA_TSV_ATIVO_NA_DTEVENTO
    REGRA:REGRA_VINCULO_ATIVO_NA_DTEVENTO"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.evtexprisco"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco"

    eso11_ideEvento = fields.Many2one(
        comodel_name="eso.11.tideeventotrab",
        string="ideEvento",
        xsd_required=True,
        xsd_type="T_ideEvento_trab",
    )

    eso11_ideEmpregador = fields.Many2one(
        comodel_name="eso.11.tideempregador",
        string="ideEmpregador",
        xsd_required=True,
        xsd_type="T_ideEmpregador",
    )

    eso11_ideVinculo = fields.Many2one(
        comodel_name="eso.11.tidevinculosst",
        string="ideVinculo",
        xsd_required=True,
        xsd_type="T_ideVinculo_sst",
    )

    eso11_infoExpRisco = fields.Many2one(
        comodel_name="eso.11.infoexprisco",
        string="Ambiente de trabalho",
        xsd_required=True,
        help=(
            "Ambiente de trabalho, atividades desempenhadas e exposição a "
            "agentes nocivos\nDESCRICAO_COMPLETA:Informações sobre o ambiente "
            "de trabalho, atividades desempenhadas e exposição a agentes "
            "nocivos.\nREGRA:REGRA_PERIODO_EXPOSICAO_RISCO\nCHAVE_GRUPO: "
            "{dtIniCondicao*}"
        ),
    )

    eso11_Id = fields.Char(string="Id", xsd_required=True, xsd_type="TS_Id")


class InfoExpRisco(models.AbstractModel):
    """Ambiente de trabalho, atividades desempenhadas e exposição a agentes
    nocivos
    DESCRICAO_COMPLETA:Informações sobre o ambiente de trabalho, atividades
    desempenhadas e exposição a agentes nocivos.
    REGRA:REGRA_PERIODO_EXPOSICAO_RISCO
    CHAVE_GRUPO: {dtIniCondicao*}"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.infoexprisco"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco"

    eso11_dtIniCondicao = fields.Date(
        string="data em que o trabalhador iniciou",
        xsd_required=True,
        xsd_type="xs:date",
        help=(
            "data em que o trabalhador iniciou as atividades nas condições "
            "descritas ou a data de início da obrigatoriedade deste evento "
            "para o empregador no eSocial, a que for mais recente.\nValidação:"
            " Deve ser uma data válida, igual ou posterior à data de admissão "
            "do vínculo a que se refere. Não pode ser anterior à data de "
            "início da obrigatoriedade deste evento para o empregador no "
            "eSocial, nem pode ser posterior a 30 (trinta) dias da data atual."
        ),
    )

    eso11_dtFimCondicao = fields.Date(
        string="data em que o trabalhador terminou",
        xsd_type="xs:date",
        help=(
            "data em que o trabalhador terminou as atividades nas condições "
            "descritas.\nValidação: Preenchimento obrigatório e exclusivo para"
            " trabalhador avulso (código de categoria no RET igual a [2XX]) e "
            "se {dtIniCondicao}(./dtIniCondicao) for igual ou posterior a "
            "[2023-01-16]. Se informada, deve ser uma data válida, igual ou "
            "posterior a {dtIniCondicao}(./dtIniCondicao) e igual ou anterior "
            "a {dtTerm}(2399_infoTSVTermino_dtTerm) de S-2399, se existente."
        ),
    )

    eso11_infoAmb = fields.One2many(
        "eso.11.infoamb",
        "eso11_infoAmb_infoExpRisco_id",
        string="Informações relativas ao ambiente",
        help=(
            "Informações relativas ao ambiente de "
            "trabalho.\nDESCRICAO_COMPLETA:Informações relativas ao ambiente "
            "de trabalho. Somente no caso de trabalhador avulso (código de "
            "categoria no RET igual a [2XX]) é possível declarar mais de um "
            "ambiente.\nCHAVE_GRUPO: {tpInsc}, "
            "{nrInsc}\nREGRA:REGRA_AMBIENTE_TRABALHO"
        ),
    )

    eso11_infoAtiv = fields.Many2one(
        comodel_name="eso.11.infoativ",
        string="Descrição das atividades desempenhadas",
        xsd_required=True,
    )

    eso11_agNoc = fields.One2many(
        "eso.11.agnoc",
        "eso11_agNoc_infoExpRisco_id",
        string="Agente(s) nocivo(s) ao(s) qual(is)",
        help=(
            "Agente(s) nocivo(s) ao(s) qual(is) o trabalhador está "
            "exposto.\nCHAVE_GRUPO: {codAgNoc}, {dscAgNoc}"
        ),
    )

    eso11_respReg = fields.One2many(
        "eso.11.respreg",
        "eso11_respReg_infoExpRisco_id",
        string="Responsável pelos registros ambientais",
        help=(
            "Responsável pelos registros "
            "ambientais\nDESCRICAO_COMPLETA:Informações relativas ao "
            "responsável pelos registros ambientais.\nCHAVE_GRUPO: {cpfResp}"
        ),
    )

    eso11_obs = fields.Many2one(
        comodel_name="eso.11.obs",
        string="Observações relativas",
        help=("Observações relativas a registros ambientais.\nCONDICAO_GRUPO: OC"),
    )


class InfoAmb(models.AbstractModel):
    """Informações relativas ao ambiente de trabalho.
    DESCRICAO_COMPLETA:Informações relativas ao ambiente de trabalho. Somente no
    caso de trabalhador avulso (código de categoria no RET igual a [2XX]) é
    possível declarar mais de um ambiente.
    CHAVE_GRUPO: {tpInsc}, {nrInsc}
    REGRA:REGRA_AMBIENTE_TRABALHO"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.infoamb"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco.InfoAmb"

    eso11_localAmb = fields.Selection(
        INFOAMB_LOCALAMB, string="localAmb", xsd_required=True
    )

    eso11_dscSetor = fields.Char(
        string="Descrição do lugar administrativo",
        xsd_required=True,
        xsd_type="TS_texto_100",
        help=(
            "Descrição do lugar administrativo, na estrutura organizacional da"
            " empresa, onde o trabalhador exerce suas atividades laborais."
        ),
    )

    eso11_tpInsc = fields.Selection(
        TS_TPINSC_1_3_4, string="tpInsc", xsd_required=True, xsd_type="TS_tpInsc_1_3_4"
    )

    eso11_nrInsc = fields.Char(
        string="Número de inscrição onde está localizado",
        xsd_required=True,
        xsd_type="TS_nrInsc_12_14",
        help=(
            "Número de inscrição onde está localizado o ambiente.\nValidação: "
            "Deve ser um identificador válido, compatível com o conteúdo do "
            "campo {infoAmb/tpInsc}(./tpInsc) e:\na) Se {localAmb}(./localAmb)"
            " = [1], deve ser válido e existente na Tabela de Estabelecimentos"
            " (S-1005);\nb) Se {localAmb}(./localAmb) = [2], deve ser "
            "diferente dos estabelecimentos informados na Tabela S-1005 e, se "
            "{infoAmb/tpInsc}(./tpInsc) = [1] e o empregador for pessoa "
            "jurídica, a raiz do CNPJ informado deve ser diferente da "
            "constante em S-1000."
        ),
    )


class InfoAtiv(models.AbstractModel):
    "Descrição das atividades desempenhadas."
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.infoativ"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco.InfoAtiv"

    eso11_dscAtivDes = fields.Char(
        string="Descrição das atividades",
        xsd_required=True,
        xsd_type="TS_texto_999",
        help=(
            "Descrição das atividades, físicas ou mentais, realizadas pelo "
            "trabalhador, por força do poder de comando a que se submete. As "
            "atividades deverão ser escritas com exatidão, e de forma sucinta,"
            " com a utilização de verbos no infinitivo impessoal. Ex.: "
            "Distribuir panfletos, operar máquina de envase, etc."
        ),
    )


class AgNoc(models.AbstractModel):
    """Agente(s) nocivo(s) ao(s) qual(is) o trabalhador está exposto.
    CHAVE_GRUPO: {codAgNoc}, {dscAgNoc}"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.agnoc"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco.AgNoc"

    eso11_codAgNoc = fields.Char(string="codAgNoc", xsd_required=True)

    eso11_dscAgNoc = fields.Char(
        string="Descrição do agente nocivo",
        xsd_type="TS_texto_100",
        help=(
            "Descrição do agente nocivo.\nValidação: Preenchimento obrigatório"
            " se {codAgNoc}(./codAgNoc) = [01.01.001, 01.02.001, 01.03.001, "
            "01.04.001, 01.05.001, 01.06.001, 01.07.001, 01.08.001, 01.09.001,"
            " 01.10.001, 01.12.001, 01.13.001, 01.14.001, 01.15.001, "
            "01.16.001, 01.17.001, 01.18.001, 05.01.001]."
        ),
    )

    eso11_tpAval = fields.Selection(AGNOC_TPAVAL, string="tpAval")

    eso11_intConc = fields.Float(string="intConc")

    eso11_limTol = fields.Float(string="limTol")

    eso11_unMed = fields.Selection(AGNOC_UNMED, string="unMed")

    eso11_tecMedicao = fields.Char(string="tecMedicao")

    eso11_epcEpi = fields.Many2one(
        comodel_name="eso.11.epcepi",
        string="EPC e EPI",
        help=(
            "EPC e EPI\nDESCRICAO_COMPLETA:Informações relativas a "
            "Equipamentos de Proteção Coletiva - EPC e Equipamentos de "
            "Proteção Individual - EPI.\nCONDICAO_GRUPO: N (se "
            "{codAgNoc}(../codAgNoc) = [09.01.001]); O (nos demais casos)"
        ),
    )


class EpcEpi(models.AbstractModel):
    """EPC e EPI
    DESCRICAO_COMPLETA:Informações relativas a Equipamentos de Proteção Coletiva -
    EPC e Equipamentos de Proteção Individual - EPI.
    CONDICAO_GRUPO: N (se {codAgNoc}(../codAgNoc) = [09.01.001]); O (nos demais
    casos)"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.epcepi"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco.AgNoc.EpcEpi"

    eso11_utilizEPC = fields.Selection(
        EPCEPI_UTILIZEPC, string="utilizEPC", xsd_required=True
    )

    eso11_eficEpc = fields.Selection(
        TS_SIM_NAO,
        string="Os EPCs são eficazes na neutralização",
        xsd_type="TS_sim_nao",
        help=(
            "Os EPCs são eficazes na neutralização do risco ao "
            "trabalhador?\nValidação: Preenchimento obrigatório e exclusivo se"
            " {utilizEPC}(./utilizEPC) = [2]."
        ),
    )

    eso11_utilizEPI = fields.Selection(
        EPCEPI_UTILIZEPI, string="utilizEPI", xsd_required=True
    )

    eso11_eficEpi = fields.Selection(
        TS_SIM_NAO,
        string="Os EPIs são eficazes na neutralização",
        xsd_type="TS_sim_nao",
        help=(
            "Os EPIs são eficazes na neutralização do risco ao "
            "trabalhador?\nValidação: Preenchimento obrigatório e exclusivo se"
            " {utilizEPI}(./utilizEPI) = [2]."
        ),
    )

    eso11_epi = fields.One2many(
        "eso.11.epi",
        "eso11_epi_epcEpi_id",
        string="EPI",
        help=(
            "EPI.\nCONDICAO_GRUPO: O (se {utilizEPI}(../utilizEPI) = [2]); N "
            "(nos demais casos)\nCHAVE_GRUPO: {docAval}"
        ),
    )

    eso11_epiCompl = fields.Many2one(
        comodel_name="eso.11.epicompl",
        string="Requisitos das NR-06",
        help=(
            "Requisitos das NR-06 e NR-09 pelo(s) EPI(s) "
            "informado(s)\nDESCRICAO_COMPLETA:Requisitos da Norma "
            "Regulamentadora 06 - NR-06 e da Norma Regulamentadora 09 - NR-09 "
            "pelo(s) EPI(s) informado(s).\nCONDICAO_GRUPO: O (se "
            "{utilizEPI}(../utilizEPI) = [2]); N (nos demais casos)"
        ),
    )


class Epi(models.AbstractModel):
    """EPI.
    CONDICAO_GRUPO: O (se {utilizEPI}(../utilizEPI) = [2]); N (nos demais casos)
    CHAVE_GRUPO: {docAval}"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.epi"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco.AgNoc.EpcEpi.Epi"

    eso11_docAval = fields.Char(
        string="Certificado de Aprovação",
        xsd_required=True,
        xsd_type="TS_texto_255",
        help=("Certificado de Aprovação - CA ou documento de avaliação do EPI."),
    )


class EpiCompl(models.AbstractModel):
    """Requisitos das NR-06 e NR-09 pelo(s) EPI(s) informado(s)
    DESCRICAO_COMPLETA:Requisitos da Norma Regulamentadora 06 - NR-06 e da Norma
    Regulamentadora 09 - NR-09 pelo(s) EPI(s) informado(s).
    CONDICAO_GRUPO: O (se {utilizEPI}(../utilizEPI) = [2]); N (nos demais casos)"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.epicompl"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco.AgNoc.EpcEpi.EpiCompl"

    eso11_medProtecao = fields.Selection(
        TS_SIM_NAO,
        string="Foi tentada a implementação de medidas",
        xsd_required=True,
        xsd_type="TS_sim_nao",
        help=(
            "Foi tentada a implementação de medidas de proteção coletiva, de "
            "caráter administrativo ou de organização, optando-se pelo EPI por"
            " inviabilidade técnica, insuficiência ou interinidade, ou ainda "
            "em caráter complementar ou emergencial?"
        ),
    )

    eso11_condFuncto = fields.Selection(
        TS_SIM_NAO,
        string="Foram observadas as condições",
        xsd_required=True,
        xsd_type="TS_sim_nao",
        help=(
            "Foram observadas as condições de funcionamento do EPI ao longo do"
            " tempo, conforme especificação técnica do fabricante nacional ou "
            "importador, ajustadas às condições de campo?"
        ),
    )

    eso11_usoInint = fields.Selection(
        TS_SIM_NAO,
        string="Foi observado o uso ininterrupto do EPI",
        xsd_required=True,
        xsd_type="TS_sim_nao",
        help=(
            "Foi observado o uso ininterrupto do EPI ao longo do tempo, "
            "conforme especificação técnica do fabricante nacional ou "
            "importador, ajustadas às condições de campo?"
        ),
    )

    eso11_przValid = fields.Selection(
        TS_SIM_NAO,
        string="Foi observado o prazo de validade do CA",
        xsd_required=True,
        xsd_type="TS_sim_nao",
        help=(
            "Foi observado o prazo de validade do CA no momento da compra do " "EPI?"
        ),
    )

    eso11_periodicTroca = fields.Selection(
        TS_SIM_NAO,
        string="É observada a periodicidade",
        xsd_required=True,
        xsd_type="TS_sim_nao",
        help=(
            "É observada a periodicidade de troca definida pelo fabricante "
            "nacional ou importador e/ou programas ambientais, comprovada "
            "mediante recibo assinado pelo usuário em época própria?"
        ),
    )

    eso11_higienizacao = fields.Selection(
        TS_SIM_NAO,
        string="É observada",
        xsd_required=True,
        xsd_type="TS_sim_nao",
        help=(
            "É observada a higienização conforme orientação do fabricante "
            "nacional ou importador?"
        ),
    )


class RespReg(models.AbstractModel):
    """Responsável pelos registros ambientais
    DESCRICAO_COMPLETA:Informações relativas ao responsável pelos registros
    ambientais.
    CHAVE_GRUPO: {cpfResp}"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.respreg"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco.RespReg"

    eso11_cpfResp = fields.Char(
        string="o CPF do responsável",
        xsd_required=True,
        xsd_type="TS_cpf",
        help=(
            "o CPF do responsável pelos registros ambientais.\nValidação: Deve"
            " ser um CPF válido."
        ),
    )

    eso11_ideOC = fields.Selection(RESPREG_IDEOC, string="ideOC")

    eso11_dscOC = fields.Char(string="dscOC")

    eso11_nrOC = fields.Char(string="nrOC")

    eso11_ufOC = fields.Selection(
        TS_UF,
        string="Sigla da Unidade da Federação",
        xsd_type="TS_uf",
        help=(
            "Sigla da Unidade da Federação - UF do órgão de "
            "classe.\nValidação: Preenchimento obrigatório se "
            "{codAgNoc}(../agNoc_codAgNoc) for diferente de [09.01.001]."
        ),
    )


class Obs(models.AbstractModel):
    """Observações relativas a registros ambientais.
    CONDICAO_GRUPO: OC"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.obs"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExpRisco.InfoExpRisco.Obs"

    eso11_obsCompl = fields.Char(
        string="obsCompl",
        xsd_required=True,
        xsd_type="TS_texto_999",
        help=(
            "Observação(ões) complementar(es) referente(s) a registros " "ambientais."
        ),
    )
