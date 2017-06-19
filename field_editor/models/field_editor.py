# -*- coding: utf-8 -*-

from odoo import models, api, _, fields

class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(res_partner, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                          toolbar=toolbar, submenu=submenu)
        view_details = self.env.get('ir.model.fields').custom_field_details('res.partner', view_type, result)
        result['fields'].update(view_details['fields'])
        if view_type in ('form', 'tree', 'search'):
            result['arch'] = view_details['arch']
        return result


# class sale_order(models.Model):
#     _inherit = 'sale.order'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(sale_order, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                          toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('sale.order', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         for field in result['fields']:
#             if result['fields'][field]['type'] == 'selection':
#                 print result['fields'][field]['selection'], type(result['fields'][field]['selection'])
#         return result
#
#
# class purchase_order(models.Model):
#     _inherit = 'purchase.order'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(purchase_order, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                              toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('purchase.order', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         return result
#
#
# class account_invoice(models.Model):
#     _inherit = 'account.invoice'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(account_invoice, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                               toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('account.invoice', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         return result
#
#
# class product_template(models.Model):
#     _inherit = 'product.template'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(product_template, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                                toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('product.template', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         return result
#
#
# class stock_picking(models.Model):
#     _inherit = 'stock.picking'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(stock_picking, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                             toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('stock.picking', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         return result
#
#
# class account_analytic_account(models.Model):
#     _inherit = 'account.analytic.account'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(account_analytic_account, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                                        toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('account.analytic.account', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         return result
#
#
# class project_project(models.Model):
#     _inherit = 'project.project'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(project_project, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                               toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('project.project', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         return result
#
#
# class crm_lead(models.Model):
#     _inherit = 'crm.lead'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(crm_lead, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                        toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('crm.lead', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         for field in result['fields']:
#             if result['fields'][field]['type'] == 'many2many':
#                 print result['fields'][field]
#         return result


# class crm_helpdesk(models.Model):
#     _inherit = 'crm.helpdesk'
#
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(crm_helpdesk, self).fields_view_get(view_id=view_id, view_type=view_type,
#                                                            toolbar=toolbar, submenu=submenu)
#         view_details = self.env.get('ir.model.fields').custom_field_details('crm.helpdesk', view_type, result)
#         result['fields'].update(view_details['fields'])
#         if view_type in ('form', 'tree', 'search'):
#             result['arch'] = view_details['arch']
#         return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: