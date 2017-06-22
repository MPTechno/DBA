# -*- coding: utf-8 -*-
import time
from odoo import fields, models, exceptions, api
from odoo.tools.translate import _

class CodeSeven(models.Model):
    _name = 'code.seven'
    _description = 'Code 7'
    
    name = fields.Char(string='Code7')
    
class AccountAnalyticLineExt(models.Model):
    _inherit = 'account.analytic.line'
    
    code7_id = fields.Many2one('code.seven',string="Code7",required=True)
    non_code_activity = fields.Char(string='Non-Code Activity')
