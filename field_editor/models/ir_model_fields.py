# -*- coding: utf-8 -*-

from lxml import etree

from odoo import models, api, _, fields
from odoo.osv.orm import setup_modifiers


def field_details(field):
    details = {
        'required': field.required,
        'type': field.ttype,
        'string': field.field_description,
        'readonly': field.readonly
    }
    if field.ttype == 'selection':
        details.update({'selection': eval(field.selection)})
    if field.ttype in ('many2one', 'many2many'):
        details.update({'relation': field.relation})
    return {
        field.name: details
    }


def form_view_arch(view_form_fields, arch):
    old_view = """<group name="Information" col="4">"""
    new_view = old_view + """%s""" % view_form_fields
    new_arch = arch.replace(old_view, new_view)
    return new_arch


def tree_view_arch(view_tree_fields, arch):
    old_view = """</tree>"""
    new_view = """%s""" % view_tree_fields + old_view
    new_arch = arch.replace(old_view, new_view)
    return new_arch


def search_view_arch(view_search_fields, old_arch):
    arch_index = old_arch.index('/>')
    new_arch   = old_arch[:arch_index + 2] + view_search_fields + old_arch[arch_index + 2:]
    return new_arch


class ir_model_fields(models.Model):
    _inherit = 'ir.model.fields'

    sequence  = fields.Integer('Sequence')
    list_ok   = fields.Boolean('Show in List View')
    search_ok = fields.Boolean('Search View')

    @api.model
    def custom_field_details(self, model, view_type, result):
        fields = self.search([('model', '=', model), ('state', '=', 'manual')], order='sequence')
        view_form_fields, view_tree_fields, view_search_fields = '', '', ''
        for field in fields:
            view_form_fields = view_form_fields + """ <field name="%s"/>""" % field.name + '\n'
            if field.list_ok:
                view_tree_fields = view_tree_fields + """ <field name="%s"/>""" % field.name + '\n'
            if field.search_ok:
                view_search_fields = view_search_fields + """ <field name="%s"/>""" % field.name + '\n'
            result['fields'].update(field_details(field))
        if view_type in ('form', 'tree', 'search'):
            result.update(
                {'arch': eval(view_type + '_view_arch')(eval('view_' + view_type + '_fields'), result['arch'])})
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            req_fields = self.search([('model', '=', model), ('state', '=', 'manual'), ('required', '=', True)])
            for field in req_fields:
                for node in doc.xpath("//field[@name='%s']" % field.name):
                    node.set('required', "1")
                    setup_modifiers(node, result['fields'][field.name])
                result['arch'] = etree.tostring(doc)
            mm_fields = self.search([('model', '=', model), ('state', '=', 'manual'), ('ttype', '=', 'many2many')])
            for field in mm_fields:
                for node in doc.xpath("//field[@name='%s']" % field.name):
                    node.set('widget', "many2many_tags")
                    setup_modifiers(node, result['fields'][field.name])
                result['arch'] = etree.tostring(doc)

        return result