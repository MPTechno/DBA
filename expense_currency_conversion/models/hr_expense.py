# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
#from odoo.exceptions import UserError, RedirectWarning, ValidationError
#from datetime import datetime
#from werkzeug import url_encode

class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    @api.multi
    def _calculate_rate(self):
        self.non_company_currency_value = self.unit_amount * self.quantity
    @api.multi
    def _is_different_currency(self):
        for obj in self:
            company_cur = self.env.user.company_id.currency_id.id
            if obj.currency_id.id != company_cur:
                obj.is_different_currency = True
    non_company_currency_rate = fields.Float(related='currency_id.rate',string='Currency Rate')
    non_company_currency_value = fields.Float(compute=_calculate_rate,string="Non-company currency value")
    is_different_currency = fields.Boolean(compute=_is_different_currency,string="Different Curency")
    rate_applied = fields.Boolean(string="Rate Applied")
    
    @api.multi
    def apply_rate(self):
        unit_amount = self.non_company_currency_rate * self.unit_amount
        return self.write({'unit_amount': unit_amount,'rate_applied':True})
    
