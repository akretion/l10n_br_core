# -*- coding: utf-8 -*-
# Copyright 2017 Akretion
# @author Raphaël Valyi <raphael.valyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import date

from openerp import models, api
from openerp.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)


class BoletoWrapper(object):
    def __init__(self, obj, boleto_api_data):
        # wrap the object
        self._wrapped_obj = obj
        self.boleto_api_data = boleto_api_data

    def __getattr__(self, attr):
        # see if this object has attr
        # NOTE do not use hasattr, it goes into
        # infinite recurrsion
        if attr in self.__dict__:
            # this object has it
            return getattr(self, attr)
        # proxy to the wrapped object
        return getattr(self._wrapped_obj, attr)


dict_brcobranca_bank = {
    '001': 'banco_brasil',
    '041': 'banrisul',
    '237': 'bradesco',
    '104': 'caixa',
    '399': 'hsbc',
    '341': 'itau',
    '033': 'santander',
    '10': 'santander',
    '748': 'sicredi',
    # banks implemented in brcobranca but not in Python:
    '004': 'banco_nordeste',
    '021': 'banestes',
    '756': 'sicoob',
}


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    # see the list of brcobranca boleto fields:
    # https://github.com/kivanio/brcobranca/blob/master/lib/brcobranca/boleto/base.rb
    # and test a here:
    # https://github.com/kivanio/brcobranca/blob/master/spec/brcobranca/boleto/itau_spec.rb

    @api.multi
    def send_payment(self):
        boleto_list = super(AccountMoveLine, self).send_payment()
        wrapped_boleto_list = []
        for boleto in boleto_list:
            boleto_api_data = {
                  'bank': 'itau', #TODO use dict_brcobranca instead
                  'valor': boleto.valor,
                  'cedente': boleto.cedente,
                  'documento_cedente': boleto.cedente_documento,
                  'sacado': boleto.sacado_nome,
                  'sacado_documento': boleto.sacado_documento,
                  'agencia': boleto.agencia_cedente,
                  'conta_corrente': boleto.conta_cedente,
                  'convenio': boleto.convenio,
                  'numero_documento': boleto.numero_documento
            }
            wrapped_boleto_list.append(BoletoWrapper(boleto, boleto_api_data))
        return wrapped_boleto_list
