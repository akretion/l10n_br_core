# Copyright (C) 2020  Renato Lima - Akretion <renato.lima@akretion.com.br>
# Copyright (C) 2014  KMEE - www.kmee.com.br
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging
import os

from erpbrasil.base.misc import punctuation_rm

from odoo import _
from odoo.tools import config

from ..constants.fiscal import CERTIFICATE_TYPE_NFE, EVENT_ENV_HML, EVENT_ENV_PROD

_logger = logging.getLogger(__name__)

try:
    from erpbrasil.assinatura import misc
except ImportError:
    _logger.error(
        _(
            "Python Library erpbrasil.assinatura not installed!"
            "You can install it with: pip install erpbrasil.assinatura."
        )
    )


def domain_field_codes(
    field_codes,
    field_name="code_unmasked",
    delimiter=",",
    operator1="=",
    operator2="=ilike",
    code_size=8,
):
    field_codes = field_codes.replace(".", "")
    list_codes = field_codes.split(delimiter)

    domain = []

    if (
        len(list_codes) > 1
        and operator1 not in ("!=", "not ilike")
        and operator2 not in ("!=", "not ilike")
    ):
        domain += ["|"] * (len(list_codes) - 1)

    for n in list_codes:
        if len(n) == code_size:
            domain.append((field_name, operator1, n))

        if len(n) < code_size:
            domain.append((field_name, operator2, n + "%"))

    return domain


def prepare_fake_certificate_vals(
    valid=True,
    passwd="123456",
    issuer="EMISSOR A TESTE",
    country="BR",
    subject="CERTIFICADO VALIDO TESTE",
    cert_type=CERTIFICATE_TYPE_NFE,
):
    return {
        "type": cert_type,
        "subtype": "a1",
        "password": passwd,
        "file": misc.create_fake_certificate_file(
            valid, passwd, issuer, country, subject
        ),
    }


def path_edoc_company(company_id):
    db_name = company_id._cr.dbname
    filestore = config.filestore(db_name)
    return "/".join([filestore, "edoc", punctuation_rm(company_id.cnpj_cpf)])


def build_edoc_path(
    company_id, ambiente, tipo_documento, ano, mes, serie=False, numero=False
):
    caminho = path_edoc_company(company_id)

    if ambiente not in (EVENT_ENV_PROD, EVENT_ENV_HML):
        _logger.error("Ambiente não informado, salvando na pasta de Homologação!")

    if ambiente == EVENT_ENV_PROD:
        caminho = os.path.join(caminho, "producao/")
    else:
        caminho = os.path.join(caminho, "homologacao/")

    caminho = os.path.join(caminho, tipo_documento)
    caminho = os.path.join(caminho, str(ano) + "-" + str(mes) + "/")

    if serie and numero:
        caminho = os.path.join(caminho, str(serie) + "-" + str(numero) + "/")
    try:
        os.makedirs(caminho, exist_ok=True)
    except Exception as e:
        _logger.error("Falha de permissão ao acessar diretorio do e-doc {}".format(e))
    return caminho
