# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from werkzeug import url_encode

class HrExpenseRegisterPaymentWizardExt(models.TransientModel):

    _inherit = "hr.expense.register.payment.wizard"

    @api.model
    def _default_partner_id(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        expense_sheet = self.env['hr.expense.sheet'].browse(active_ids)
        if len(expense_sheet) > 1:
            return expense_sheet[0].address_id.id or expense_sheet[0].employee_id.id and expense_sheet[0].employee_id.address_home_id.id    
        return expense_sheet.address_id.id or expense_sheet.employee_id.id and expense_sheet.employee_id.address_home_id.id

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, default=_default_partner_id)
    
    @api.model
    def default_get(self, fields):
        res = super(HrExpenseRegisterPaymentWizardExt, self).default_get(fields)
        if not res.get('amount'):
            expese_report_ids = self.env.context.get('active_ids')
            total_amount = 0.0
            for report in self.env['hr.expense.sheet'].browse(expese_report_ids):
                total_amount += report.total_amount
            res.update({'amount':total_amount})
        return res
        
    @api.multi
    def expense_post_payment(self):
        self.ensure_one()
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        for expense_sheet in self.env['hr.expense.sheet'].browse(active_ids):
            # Create payment and post it
            payment = self.env['account.payment'].create({
                'partner_type': 'supplier',
                'payment_type': 'outbound',
                'partner_id': self.partner_id.id,
                'journal_id': self.journal_id.id,
                'company_id': self.company_id.id,
                'payment_method_id': self.payment_method_id.id,
                'amount': self.amount,
                'currency_id': self.currency_id.id,
                'payment_date': self.payment_date,
                'communication': self.communication
            })
            payment.post()

            # Log the payment in the chatter
            body = (_("A payment of %s %s with the reference <a href='/mail/view?%s'>%s</a> related to your expense %s has been made.") % (payment.amount, payment.currency_id.symbol, url_encode({'model': 'account.payment', 'res_id': payment.id}), payment.name, expense_sheet.name))
            expense_sheet.message_post(body=body)

            # Reconcile the payment and the expense, i.e. lookup on the payable account move lines
            account_move_lines_to_reconcile = self.env['account.move.line']
            for line in payment.move_line_ids + expense_sheet.account_move_id.line_ids:
                if line.account_id.internal_type == 'payable':
                    account_move_lines_to_reconcile |= line
            account_move_lines_to_reconcile.reconcile()
        return {'type': 'ir.actions.act_window_close'}

