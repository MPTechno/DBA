# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models
import calendar

class expense_sheet_report_dba(models.AbstractModel):
    _name = 'report.dba_multi_expese_report.expense_sheet_report'

    @api.multi
    def _get_expense_sheet_report_data(self,data):#,
        expense_objs = self.env['hr.expense.sheet'].browse(data.get('ids'))
        result = []
        for expense_obj in expense_objs:
            for expense in expense_obj.expense_line_ids:
                result.append(expense)
        return result
    
    @api.multi
    def _get_employee_name(self, data):
        if data.has_key('ids') and data.get('ids'):
            employee_name = self.env['hr.expense.sheet'].browse(data.get('ids')[0]).employee_id.name
            return employee_name
        else:
            return ''

    @api.multi
    def _get_total(self, data):
        expense_objs = self.env['hr.expense.sheet'].browse(data.get('ids'))
        total = 0.00
        for expense_obj in expense_objs:
            for line in expense_obj.expense_line_ids:
                total += line.total_amount
        return total
        
    @api.multi
    def _get_currency_symbol(self, data):
        if data.has_key('ids') and data.get('ids'):
            currency_symbol = self.env['hr.expense.sheet'].browse(data.get('ids')[0]).currency_id.symbol
            return currency_symbol
        else:
            return ''
        

    @api.multi
    def _get_pc(self, data):
        expense_objs = self.env['hr.expense.sheet'].browse(data.get('ids'))
        result = []
        for expense_obj in expense_objs:
            if expense_obj.pc_no and str(expense_obj.pc_no) not in result:
                result.append(str(expense_obj.pc_no))
        result = str(result).replace("['",'').replace("[",'').replace("']",'').replace("]",'').replace("'",'')
        return result


    @api.multi
    def _get_cheque_no(self, data):
        expense_objs = self.env['hr.expense.sheet'].browse(data.get('ids'))
        result = []
        for expense_obj in expense_objs:
            for line in expense_obj.expense_line_ids:
                if line.cheque_no and str(line.cheque_no) not in result:
                    result.append(str(line.cheque_no))
        result = str(result).replace("['",'').replace("[",'').replace("']",'').replace("]",'').replace("'",'')
        return result
    @api.multi
    def _get_months(self,data):
        months = list(calendar.month_name)
        expense_objs = self.env['hr.expense.sheet'].browse(data.get('ids'))
        res = ''
        for expense_obj in expense_objs:
            for line in expense_obj.expense_line_ids:
                date_data = line.date.split('-')
                index = int(date_data[1])
                year = date_data[0]
                res_value = months[index] + ' ' + year + ' '
                if res_value not in res:
                    res+=  res_value
        return res
    @api.model
    def render_html(self, docids, data=None):
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.env['hr.expense.sheet'],
            'data': data,
            'docs': self.env['hr.expense.sheet'].browse(self.ids),
            'time': time,
            'get_employee_name': self._get_employee_name,
            'get_expense_sheet_report_data': self._get_expense_sheet_report_data,
            'get_total': self._get_total,
            'get_currency_symbol': self._get_currency_symbol,
            'get_pc': self._get_pc,
            'get_cheque_no': self._get_cheque_no,
            'get_months':self._get_months,
        }
        return self.env['report'].render('dba_multi_expese_report.expense_sheet_report', docargs)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

