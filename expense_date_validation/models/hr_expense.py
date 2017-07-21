# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime

class hr_expense(models.Model):
    _inherit = 'hr.expense'
    
    def _check_date(self):
        if self.date:
            today_date = datetime.now().date()
            current_date = datetime.strptime(str(today_date), '%Y-%m-%d').date()
            expense_date = datetime.strptime(self.date, '%Y-%m-%d').date()
            month = (current_date.year - expense_date.year) * 12 + current_date.month - expense_date.month
            limit = int(self.env.ref('expense_date_validation.hr_expense_submit_limit').value)
            if month >= limit:
                #raise ValidationError(_('''You can Enter only %s months older Expense than today's date. \n 
                #                            But you have entered %s months older Expense.\n
                #                            Please contact Admin to submit this Expense.''')%(limit,month))
                return False
            else:
                return True
        return True 
        
    _constraints = [(_check_date, '''You are too late to submit this expense.\nPlease contact Administrator!!!!''', ['date'])]

class HrExpenseConfigSettings(models.TransientModel):
    _inherit = 'hr.expense.config.settings'
    
    exp_sub_limit = fields.Integer('Expense Submission Period Limit(Month)')
    

    @api.model
    def get_default_exp_sub_limit(self, fields):
        limit = int(self.env.ref('expense_date_validation.hr_expense_submit_limit').value)
        return {'exp_sub_limit': limit}

    @api.multi
    def set_default_exp_sub_limit(self):
        for record in self:
            self.env.ref('expense_date_validation.hr_expense_submit_limit').write({'value': str(record.exp_sub_limit)})
    

