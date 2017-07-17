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
            if month >= 3:
                return False
            else:
                return True
        return True 
        
    _constraints = [(_check_date, 'Expense Date is 3 months more than the Current Date', ['date'])]
