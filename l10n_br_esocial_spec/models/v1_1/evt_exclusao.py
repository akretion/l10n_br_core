# Copyright 2023 Akretion - Raphaël Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
# Generated by https://github.com/akretion/xsdata-odoo
#
import textwrap
from odoo import fields, models
from .tipos import (
    TSINDAPURACAO,
    TIdeEmpregadorExclusao,
    TIdeEventoExclusao,
)

__NAMESPACE__ = "http://www.esocial.gov.br/schema/evt/evtExclusao/v_S_01_01_00"


class ESocial(models.AbstractModel):
    "S-3000 - Exclusão de Eventos"
    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.esocial"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial"

    eso11_evtExclusao = fields.Many2one(
        comodel_name="eso.11.evtexclusao",
        string="Evento Exclusão",
        xsd_required=True,
        help=(
            "Evento Exclusão\nDESCRICAO_COMPLETA:Evento Exclusão de "
            "Eventos.\nCHAVE_GRUPO: {Id}\nREGRA:REGRA_ENVIO_PROC_FECHAMENTO\nR"
            "EGRA:REGRA_EVE_EXCLUSAO_VALIDA_NRRECIBO\nREGRA:REGRA_EXISTE_INFO_"
            "EMPREGADOR\nREGRA:REGRA_EXTEMP_DOMESTICO\nREGRA:REGRA_MESMO_PROCE"
            "MI\nREGRA:REGRA_VALIDA_EMPREGADOR"
        ),
    )


class EvtExclusao(models.AbstractModel):
    """Evento Exclusão
    DESCRICAO_COMPLETA:Evento Exclusão de Eventos.
    CHAVE_GRUPO: {Id}
    REGRA:REGRA_ENVIO_PROC_FECHAMENTO
    REGRA:REGRA_EVE_EXCLUSAO_VALIDA_NRRECIBO
    REGRA:REGRA_EXISTE_INFO_EMPREGADOR
    REGRA:REGRA_EXTEMP_DOMESTICO
    REGRA:REGRA_MESMO_PROCEMI
    REGRA:REGRA_VALIDA_EMPREGADOR"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.evtexclusao"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExclusao"

    eso11_ideEvento = fields.Many2one(
        comodel_name="eso.11.tideeventoexclusao",
        string="ideEvento",
        xsd_required=True,
        xsd_type="T_ideEvento_exclusao",
    )

    eso11_ideEmpregador = fields.Many2one(
        comodel_name="eso.11.tideempregadorexclusao",
        string="ideEmpregador",
        xsd_required=True,
        xsd_type="T_ideEmpregador_exclusao",
    )

    eso11_infoExclusao = fields.Many2one(
        comodel_name="eso.11.infoexclusao",
        string="Informação do evento que será excluído",
        xsd_required=True,
        help=(
            "Informação do evento que será excluído\nDESCRICAO_COMPLETA:Grupo "
            "que identifica o evento objeto da exclusão."
        ),
    )

    eso11_Id = fields.Char(string="Id", xsd_required=True, xsd_type="TS_Id")


class InfoExclusao(models.AbstractModel):
    """Informação do evento que será excluído
    DESCRICAO_COMPLETA:Grupo que identifica o evento objeto da exclusão."""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.infoexclusao"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExclusao.InfoExclusao"

    eso11_tpEvento = fields.Char(string="tpEvento", xsd_required=True)

    eso11_nrRecEvt = fields.Char(
        string="o número do recibo do evento",
        xsd_required=True,
        xsd_type="TS_nrRecibo",
        help=(
            "o número do recibo do evento que será excluído.\nValidação: O "
            "recibo deve ser relativo ao mesmo tipo de evento indicado em "
            "{tpEvento}(./tpEvento) e o respectivo evento não deve constar "
            "como excluído ou retificado. Além disso, no caso de exclusão de "
            "eventos em que existe a identificação do trabalhador, o evento "
            "que está sendo excluído deve referir-se ao mesmo trabalhador "
            "identificado por {cpfTrab}(./ideTrabalhador_cpfTrab)."
        ),
    )

    eso11_ideTrabalhador = fields.Many2one(
        comodel_name="eso.11.idetrabalhador",
        string="Identificação do trabalhador",
        help=(
            "Identificação do trabalhador a que se refere o evento a ser "
            "excluído\nDESCRICAO_COMPLETA:Grupo que identifica a qual "
            "trabalhador se refere o evento a ser excluído.\nCONDICAO_GRUPO: O"
            " (se {tpEvento}(../tpEvento) corresponder a um dos eventos não "
            "periódicos (S-2190 a S-2420 ou S-8299) ou um dos eventos "
            "periódicos (S-1200 a S-1210); N (nos demais casos)"
        ),
    )

    eso11_ideFolhaPagto = fields.Many2one(
        comodel_name="eso.11.idefolhapagto",
        string="Identificação do período de apuração",
        help=(
            "Identificação do período de apuração a que se refere o evento que"
            " será excluído\nDESCRICAO_COMPLETA:Grupo que identifica a qual "
            "período de apuração pertence o evento que será "
            "excluído.\nCONDICAO_GRUPO: O (se {tpEvento}(../tpEvento) "
            "corresponder a um dos eventos periódicos (S-1200 a S-1280 ou "
            "S-1300)); N (nos demais casos)"
        ),
    )


class IdeTrabalhador(models.AbstractModel):
    """Identificação do trabalhador a que se refere o evento a ser excluído
    DESCRICAO_COMPLETA:Grupo que identifica a qual trabalhador se refere o evento a
    ser excluído.
    CONDICAO_GRUPO: O (se {tpEvento}(../tpEvento) corresponder a um dos eventos não
    periódicos (S-2190 a S-2420 ou S-8299) ou um dos eventos periódicos (S-1200
    a S-1210); N (nos demais casos)"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.idetrabalhador"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExclusao.InfoExclusao.IdeTrabalhador"

    eso11_cpfTrab = fields.Char(
        string="o número do CPF do trabalhador",
        xsd_required=True,
        xsd_type="TS_cpf",
        help=(
            "o número do CPF do trabalhador ou do beneficiário.\nValidação: O "
            "CPF indicado deve existir na base de dados do RET."
        ),
    )


class IdeFolhaPagto(models.AbstractModel):
    """Identificação do período de apuração a que se refere o evento que será
    excluído
    DESCRICAO_COMPLETA:Grupo que identifica a qual período de apuração pertence o
    evento que será excluído.
    CONDICAO_GRUPO: O (se {tpEvento}(../tpEvento) corresponder a um dos eventos
    periódicos (S-1200 a S-1280 ou S-1300)); N (nos demais casos)"""

    _description = textwrap.dedent("    %s" % (__doc__,))
    _name = "eso.11.idefolhapagto"
    _inherit = "spec.mixin.eso"
    _binding_type = "ESocial.EvtExclusao.InfoExclusao.IdeFolhaPagto"

    eso11_indApuracao = fields.Selection(
        TS_INDAPURACAO,
        string="Indicativo de período de apuração",
        xsd_type="TS_indApuracao",
        help=(
            "Indicativo de período de apuração.\nValidação: Preenchimento "
            "obrigatório e exclusivo se {tpEvento}(../tpEvento) = [S-1200, "
            "S-1202, S-1207, S-1280, S-1300]."
        ),
    )

    eso11_perApur = fields.Char(
        string="mês/ano",
        xsd_required=True,
        xsd_type="TS_perApur",
        help=(
            "mês/ano (formato AAAA-MM) ou apenas o ano (formato AAAA) de "
            "referência das informações.\nValidação: Deve ser um mês/ano ou "
            "ano válido, posterior à implementação do eSocial. Somente pode "
            "ser informado ano (formato AAAA) se {indApuracao}(./indApuracao) "
            "= [2]."
        ),
    )
