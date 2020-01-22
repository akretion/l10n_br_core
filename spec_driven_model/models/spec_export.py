# Copyright 2019 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from nfelib.v4_00 import leiauteNFe

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class AbstractSpecMixin(models.AbstractModel):
    _inherit = 'spec.mixin'

    def _get_ds_class(self, class_obj):
        #  FIXME: leiauteNFe hardcoded
        return getattr(leiauteNFe, class_obj._generateds_type)

    def _export_field(self, xsd_fields, class_obj, export_dict):
        ds_class = self._get_ds_class(class_obj)
        ds_class_sepc = {i.name: i for i in ds_class.member_data_items_}

        for xsd_field in xsd_fields:
            # TODO: Export number required fields with Zero.
            # xsd_required = self.env[class_name]._fields[xsd_field]._attrs.get(
            #     'xsd_required')

            # FIXME: xsd_field.replace(class_obj._field_prefix, '')
            field_spec_name = xsd_field.replace('nfe40_', '')
            member_spec = ds_class_sepc[field_spec_name]

            # if not self[xsd_field]:
            #     continue

            # print(self[xsd_field])
            # print(xsd_field)
            # print(self._fields[xsd_field].type)
            # print(member_spec.data_type[0])

            if self._fields[xsd_field].type == 'many2one':
                field_data = self._export_many2one(xsd_field, class_obj)
            elif self._fields[xsd_field].type == 'one2many':
                field_data = self._export_one2many(xsd_field, class_obj)
            elif self._fields[xsd_field].type == 'datetime' and self[xsd_field]:
                field_data = self._export_datetime(xsd_field)
            elif self._fields[xsd_field].type == 'date' and self[xsd_field]:
                field_data = self._export_date(xsd_field)
            elif self._fields[xsd_field].type in ('float', 'monetary') and self[xsd_field] is not False:
                field_data = self._export_float_monetary(
                    xsd_field, member_spec)
            else:
                field_data = self[xsd_field]

            if not self[xsd_field] and not field_data:
                continue

            # print(field_data)
            export_dict[field_spec_name] = field_data

    def _export_many2one(self, field_name, class_obj=None):
        if self._fields[field_name]._attrs.get('original_spec_model'):
            field_data = self[field_name]._build_generateds(
                class_name=self._fields[field_name]._attrs.get(
                    'original_spec_model')
            )
        else:
            # continue
            try:
                field_data = self._build_generateds(
                    class_obj._fields[field_name].comodel_name)
            except:
                field_data = self[field_name]._build_generateds(
                    class_obj._fields[field_name].comodel_name)
        return field_data

    def _export_one2many(self, field_name, class_obj=None):
        relational_data = []
        for relational_field in self[field_name]:
            relational_data.append(
                relational_field._build_generateds(
                    class_obj._fields[field_name].comodel_name
                )
            )
        return relational_data

    def _export_float_monetary(self, field_name, member_spec):
        if member_spec.data_type[0]:
            TDec = ''.join(filter(lambda x: x.isdigit(),
                                  member_spec.data_type[0]))[-2:]
            format = "%.{0}f".format(TDec)
            return str(format % self[field_name])
        else:
            raise NotImplementedError

    def _export_date(self, field_name):
        return str(self[field_name])

    def _export_datetime(self, field_name):
        return str(fields.Datetime.context_timestamp(
            self,
            fields.Datetime.from_string(self[field_name])
        ).isoformat('T'))

    def _get_model_classes(self):
        classes = [getattr(x, '_name', None) for x in type(self).mro()]
        return classes

    def _get_spec_classes(self, classes=False):
        if not classes:
            classes = self._get_model_classes()
        spec_classes = []
        for c in set(classes):
            if c is None:
                continue
            if 'nfe.' not in c:  # make generic brittle
                continue
            # the following filter to fields to show
            # when several XSD class are injected in the same object
            if self._context.get('spec_class') and c != self._context[
                'spec_class']:
                continue
            spec_classes.append(c)
        return spec_classes

    def _build_generateds(self, class_name=False):
        if not class_name:
            if hasattr(self, '_stacked'):
                class_name = self._stacked
            else:
                class_name = self._name

        class_obj = self.env[class_name]
        if not class_obj._generateds_type:
            return

        xsd_fields = (
            i for i in self.env[class_name]._fields if
            self.env[class_name]._fields[i]._attrs.get('xsd')
        )

        kwargs = {}

        ds_class = self._get_ds_class(class_obj)
        self._export_field(xsd_fields, class_obj, export_dict=kwargs)

        if kwargs:
            ds_object = ds_class(**kwargs)
            return ds_object

    def _print_xml(self, ds_object):
        if not ds_object:
            return
        output = StringIO()
        ds_object.export(
            output,
            0,
            pretty_print=True,
        )
        contents = output.getvalue()
        output.close()
        print(contents)

    def export_xml(self):
        if hasattr(self, '_stacked'):
            ds_object = self._build_generateds()
            self._print_xml(ds_object)
        else:
            spec_classes = self._get_spec_classes()
            ds_objects = []
            for class_name in spec_classes:
                ds_object = self._build_generateds(class_name)
                self._print_xml(ds_object)
                ds_objects.append(ds_object)
