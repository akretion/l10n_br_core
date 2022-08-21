# Copyright 2022 Engenere
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import operator
import re
from unidecode import unidecode

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval, time


class CNABField(models.Model):

    _name = "l10n_br_cnab.line.field"
    _description = "Fields in CNAB lines."

    name = fields.Char(readonly=True, states={"draft": [("readonly", False)]})

    ref_name = fields.Char(
        string="Reference Name",
        help="Unique reference name to identify the cnab field, can be used to search"
        " the field content in python expressions in 'Dynamic Content'. "
        "It is generated automatically by aggregating the field name, starting "
        "position and ending position. ex:. 'field_name_001-015'",
        compute="_compute_ref_name",
    )

    meaning = fields.Char(readonly=True, states={"draft": [("readonly", False)]})
    cnab_line_id = fields.Many2one(
        "l10n_br_cnab.line",
        readonly=True,
        ondelete="cascade",
        required=True,
        states={"draft": [("readonly", False)]},
    )
    start_pos = fields.Integer(
        string="Start Position",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    end_pos = fields.Integer(
        string="End Position",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type = fields.Selection(
        [
            ("alpha", _("Alphanumeric")),
            ("num", _("Numeric")),
        ],
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    related_field_id = fields.Many2one(
        "ir.model.fields", readonly=True, states={"draft": [("readonly", False)]}
    )
    default_value = fields.Char(readonly=True, states={"draft": [("readonly", False)]})
    notes = fields.Char(readonly=True, states={"draft": [("readonly", False)]})
    size = fields.Integer(compute="_compute_size")

    state = fields.Selection(
        selection=[("draft", "Draft"), ("review", "Review"), ("approved", "Approved")],
        readonly=True,
        default="draft",
    )
    content_source_model_id = fields.Many2one(
        comodel_name="ir.model", related="cnab_line_id.content_source_model_id"
    )
    content_source_field = fields.Char(
        string="Content Source Field",
        help="Inform the field with the origin of the content, expressed with dot notation.",
    )

    preview_field = fields.Char(compute="_compute_preview_field")

    resource_ref = fields.Reference(
        string="Reference",
        related="cnab_line_id.resource_ref",
    )

    dynamic_content = fields.Char(
        help="Expression in Python to define the final value of the content,"
        "you can use the following predefined words: \n\n"
        "'content' returns the value of the mapped content source field. \n"
        "'time' class to handle date. \n"
        "'seq_batch' returns the batch sequence. \n"
        "'seq_batch_record' returns the sequence for record in the batch. \n"
        "'qty_batch_records' returns the number of records in the batch \n"
        "'batch_lines' returns a list of dicts, each dict corresponds to a record in "
        "the batch, each item in the dict corresponds to a cnab field. the key is the"
        " reference name and the value is the content."
    )

    def action_change_field(self):
        "action for change for field"
        return {
            "name": _("Change Dot Notation Field"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "res_model": "field.select.wizard",
            "target": "new",
            "context": {
                "default_cnab_field_id": self.id,
                "default_content_source_field": self.content_source_field,
            },
        }

    def _compute_ref_name(self):
        for rec in self:
            name = unidecode(rec.name.replace(" ", "_").lower())
            rec.ref_name = f"{name}_{rec.start_pos}_{rec.end_pos}"

    @api.depends("resource_ref", "content_source_field", "dynamic_content")
    def _compute_preview_field(self):
        for rec in self:
            preview = ""
            if rec.resource_ref:
                try:
                    ref_name, preview = rec.output(rec.resource_ref)
                    preview = preview.replace(" ", "⎵")
                except (ValueError, SyntaxError) as exc:
                    preview = str(exc)
            rec.preview_field = preview

    def output(self, resource_ref, **kwargs):
        "Compute output value for this field"
        for rec in self:
            value = ""
            if rec.content_source_field and resource_ref:
                value = (
                    operator.attrgetter(rec.content_source_field)(resource_ref) or ""
                )
            if rec.dynamic_content:
                value = rec.eval_compute_value(value, **kwargs)
            value = self.format(rec.size, rec.type, value)

            return self.ref_name, value

    def format(self, size, value_type, value):
        """formats the value according to the specification"""
        value = str(value)
        if value_type == "num":
            value = re.sub(r"\W+", "", value)
        value = value[:size]
        if value_type == "num":
            value = value.zfill(size)
        if value_type == "alpha":
            value = value.ljust(size)
        return value

    def eval_compute_value(self, value, **kwargs):
        "Execute python code and return computed value"
        self.ensure_one()
        safe_eval_dict = {
            "value": value,
            "time": time,
            "seq_batch": kwargs.get("seq_batch", ""),
            "seq_batch_record": kwargs.get("seq_batch_record", ""),
            "qty_batch_records": kwargs.get("qty_batch_records", ""),
            "batch_lines": kwargs.get("batch_lines", []),
        }
        return safe_eval(self.dynamic_content, safe_eval_dict)

    @api.depends("start_pos", "end_pos")
    def _compute_size(self):
        for f in self:
            f.size = f.end_pos - f.start_pos + 1

    def unlink(self):
        lines = self.filtered(lambda l: l.state != "draft")
        if lines:
            raise UserError(_("You cannot delete an CNAB Field which is not draft !"))
        return super(CNABField, self).unlink()

    def action_review(self):
        self.write({"state": "review"})

    def action_approve(self):
        self.write({"state": "approved"})

    def action_draft(self):
        self.write({"state": "draft"})

    def check_field(self):
        if self.start_pos > self.end_pos:
            raise UserError(
                _(
                    f"{self.name} in {self.cnab_line_id}: Start position is greater than end position."
                )
            )
