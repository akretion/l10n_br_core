# (c) 2014 Kmee - Luis Felipe Mileo <mileo@kmee.com.br>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class HrEducationalAttainment(models.Model):
    _name = 'hr.educational.attainment'
    _description = 'Educational Attainments'

    name = fields.Char(
        string='Educational Attainment')

    code = fields.Char(
        string='Code')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            result.append((record['id'], name))
        return result
