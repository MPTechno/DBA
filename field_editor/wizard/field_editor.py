# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from lxml import etree

class field_editor(models.TransientModel):
    _name        = 'field.editor'
    _description = 'Field Editor'

    def _get_fields(self):
        field_list = []
        model = self._context['active_model']
        if 'edit' in self._context:
            field_ids = self.env['ir.model.fields'].search([('model', '=', model), ('state', '=', 'manual')], order='sequence')
            for field in field_ids:
                field_list.append({
                    'label': field.field_description,
                    'type': field.ttype,
                    'required': field.required,
                    'field_id': field.id,
                    'sequence': field.sequence,
                    'list_ok': field.list_ok,
                    'search_ok': field.search_ok,
                    'required': field.required
                })
        return field_list

    label = fields.Char('Field Label')
    type  = fields.Selection([
        ('char', 'Text'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('float', 'Float'),
        ('integer', 'Integer'),
        ('boolean', 'Checkbox'),
        ('selection', 'Dropdown(Pre-defined)'),
        ('many2one', 'Dropdown'),
        ('many2many', 'Multi-select')
    ], 'Field Type')
    line_ids  = fields.One2many('field.editor.lines', 'editor_id', 'Lines', default=_get_fields)
    selection = fields.Char('Dropdown List')
    list_ok   = fields.Boolean('Show in List View')
    search_ok = fields.Boolean('Search View')
    required  = fields.Boolean('Compulsory')
    model_id  = fields.Many2one('ir.model', 'Relation')

    @api.multi
    def action_create_field(self):
        field_obj = self.env['ir.model.fields']
        model     = self._context['active_model']
        model_id  = self.env['ir.model'].search([('model', '=', model)])[0].id
        field_ids = field_obj.search([('model', '=', model), ('state', '=', 'manual')], order='sequence')
        sequences = [field.sequence for field in field_ids]
        sequence  = sequences and sequences[-1] + 1 or 1
        label     = self.label
        name      = 'x_' + label.replace(' ', '_').lower()

        field_vals = {
            'name'              : name,
            'field_description' : label,
            'ttype'             : self.type,
            'model_id'          : model_id,
            'state'             : 'manual',
            'sequence'          : sequence,
            'list_ok'           : self.list_ok,
            'search_ok'         : self.search_ok,
            'required'          : self.required
        }
        if self.type == 'selection':
            selection_list = []
            for selection in self.selection.split(','):
                selection_list.append((str(selection), selection))
            field_vals.update({
                'selection': str(selection_list)
            })
        if self.type in ('many2one', 'many2many'):
            field_vals.update({
                'relation': str(self.model_id.model)
            })
        field_obj.create(field_vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.multi
    def action_update_field(self):
        for line in self.line_ids:
            if line.delete_ok:
                line.field_id.unlink()
                continue
            line.field_id.write({
                'sequence'          : line.sequence,
                'field_description' : line.label,
                'ttype'             : line.type,
                'list_ok'           : line.list_ok,
                'search_ok'         : line.search_ok,
                'required'          : line.required
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

class field_editor_lines(models.TransientModel):
    _name        = 'field.editor.lines'
    _description = 'Field Editor Lines'
    _order       = 'sequence'

    editor_id = fields.Many2one('field.editor', 'Editor')
    label     = fields.Char('Label')
    type      = fields.Selection([
        ('char', 'Text'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('float', 'Float'),
        ('integer', 'Integer'),
        ('boolean', 'Checkbox'),
        ('selection', 'Dropdown(Pre-defined)'),
        ('many2one', 'Dropdown'),
        ('many2many', 'Multi-select')
    ], 'Field Type')
    sequence  = fields.Integer('Sequence')
    delete_ok = fields.Boolean('Delete')
    field_id  = fields.Many2one('ir.model.fields', 'Field ID')
    list_ok   = fields.Boolean('Show in List View')
    search_ok = fields.Boolean('Search View')
    required  = fields.Boolean('Compulsory')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: