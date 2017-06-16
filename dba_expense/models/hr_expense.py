# -*- coding: utf-8 -*-
# Part of GYB IT Solutions.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime

class hr_expense(models.Model):
    _inherit = 'hr.expense'
	
	
    paid_by = fields.Selection([('Cash','Cash'),('Cheque','Cheque')],'Paid By', default='Cash')
    cheque_no = fields.Char('Cheque No')
    pc_no = fields.Text('PC#')
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            if not self.name:
                self.name = self.product_id.display_name or ''
            if self.product_id.name == 'Medical':
                self.unit_amount = self.env['medical.claim.limit'].search([])[0].medical_claim_limit
            else:
                self.unit_amount = self.product_id.price_compute('standard_price')[self.product_id.id]
            self.product_uom_id = self.product_id.uom_id
            self.tax_ids = self.product_id.supplier_taxes_id
            account = self.product_id.product_tmpl_id._get_product_accounts()['expense']
            if account:
                self.account_id = account
    
    
    @api.depends('quantity', 'unit_amount', 'tax_ids', 'currency_id','product_id')
    def _compute_amount(self):
        for expense in self:
            if expense.product_id.name == 'Medical':
                expense.total_amount = self.env['medical.claim.limit'].search([])[0].medical_claim_limit
            else:
                expense.untaxed_amount = expense.unit_amount * expense.quantity
                taxes = expense.tax_ids.compute_all(expense.unit_amount, expense.currency_id, expense.quantity, expense.product_id, expense.employee_id.user_id.partner_id)
                expense.total_amount = taxes.get('total_included')
    
    
    @api.one
    @api.constrains('date')
    def _check_date(self):
        if self.date:
            today_date = datetime.now().date()
            current_date = datetime.strptime(str(today_date), '%Y-%m-%d').date()
            expense_date = datetime.strptime(self.date, '%Y-%m-%d').date()
            month = (current_date.year - expense_date.year) * 12 + current_date.month - expense_date.month
            if month >= 3:
                raise ValidationError(_('Expense Date is 3 months more than the Current Date !'))
	

class medical_claim_limit(models.Model):
    _name = 'medical.claim.limit'
    
    medical_claim_limit = fields.Float('Medical Claim Limit',required=True)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
