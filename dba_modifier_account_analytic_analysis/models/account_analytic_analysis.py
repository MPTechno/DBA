# -*- coding: utf-8 -*-
# Part of GYB IT Solutions.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'
    
    contract_category_id = fields.Many2one('contract.category', string='Category')
    description = fields.Char('Description')
    date_end = fields.Date('Expiration Date')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Project Code already exists !'),
    ]


class contract_category(models.Model):
    _name = 'contract.category'
    _description = 'Contract Category'
    
    name = fields.Char('Name', required=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
