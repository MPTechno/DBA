# -*- coding: utf-8 -*-
import time
from odoo import fields, models, exceptions, api
from odoo.tools.translate import _

class CodeSeven(models.Model):
    _name = 'code.seven'
    _description = 'Code 7'
    
    name = fields.Char(string='Code7')
    
#    @api.multi
#    def name_get(self):
#        result = []
#        count = 1
#        for rec in self:
#            name = str(count) + '-' + rec.name 
#            result.append((rec.id, name))
#            count+= 1
#        return result
    
class AccountAnalyticLineExt(models.Model):
    _inherit = 'account.analytic.line'
    
    code7_id = fields.Many2one('code.seven',string="Code7",required=True)
    non_code_activity = fields.Char(string='Non-Code Activity')
    
