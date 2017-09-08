# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime
from werkzeug import url_encode

class hr_expense(models.Model):
    _inherit = 'hr.expense'
	
    paid_by = fields.Selection([('Cash','Cash'),('Cheque','Cheque')],'Paid By', default='Cash')
    cheque_no = fields.Char('Cheque No')
    manager_id = fields.Many2one('hr.employee','Approver')
    submit_to_accountant = fields.Boolean('Submitted',readonly=True)
    billable = fields.Selection([('yes','Billable'),('no','Non-Billable')],'Bill Type',default='no')
    
    @api.multi
    def write(self, values):
        def check_exp_limit(total):
            if self.product_id.expense_limit != 0.0 and total > self.product_id.expense_limit:
                raise UserError(_("You can't add more expense than %s !") % (self.product_id.expense_limit))
        if values.get('quantity') and values.get('unit_amount'):
            total = values.get('unit_amount') * values.get('quantity')
            check_exp_limit(total)
        elif values.get('unit_amount'):
            total = self.quantity * values.get('unit_amount')
            check_exp_limit(total)
        elif values.get('quantity'):
            total = self.unit_amount * values.get('quantity')
            check_exp_limit(total)
        return super(hr_expense, self).write(values)
    
    @api.model
    def create(self, vals):
        product_obj = self.env['product.product'].browse(vals.get('product_id'))
        total_exp = vals.get('unit_amount') * vals.get('quantity')
        if product_obj.expense_limit != 0.0 and total_exp > product_obj.expense_limit:
            raise UserError(_("You can't add more expense than %s !") % (product_obj.expense_limit))
        else:
            hr_expense_obj = super(hr_expense, self).create(vals)
            return hr_expense_obj
    
    
    @api.multi
    def submit_expenses(self):
        for obj in self:
            if obj.product_id.expense_limit != 0.0 and obj.total_amount > obj.product_id.expense_limit:
                raise UserError(_("You can't add more expense than %s !") % (obj.product_id.expense_limit))
            if not obj.manager_id:
                raise ValidationError(_('Please Selet the Approver to Approve !'))
        if any(expense.state != 'draft' for expense in self):
            raise UserError(_("You cannot report twice the same line!"))
        if len(self.mapped('employee_id')) != 1:
            raise UserError(_("You cannot report expenses for different employees in the same report!"))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.expense.sheet',
            'target': 'current',
            'context': {
                'default_expense_line_ids': [line.id for line in self],
                'default_employee_id': self[0].employee_id.id,
                'default_name': self[0].name if len(self.ids) == 1 else ''
            }
        }
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            if not self.name:
                self.name = self.product_id.display_name or ''
            if self.product_id.expense_limit:
                self.unit_amount = self.product_id.expense_limit
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
            expense.total_amount = expense.unit_amount * expense.quantity
            expense.untaxed_amount = expense.unit_amount * expense.quantity
            taxes = expense.tax_ids.compute_all(expense.unit_amount, expense.currency_id, expense.quantity, expense.product_id, expense.employee_id.user_id.partner_id)
            expense.total_amount = taxes.get('total_included')
    
    
    @api.multi
    def get_accountant(self):
        res_groups = self.env['res.groups']
        group_id = res_groups.search([('name','=','Accountant')])
        partners = []
        if group_id:
            for partner in group_id.users:
                partners.append(partner.partner_id.id)
        return partners[0]
    
    
    @api.multi
    def submit_to_account(self):
        self.submit_to_accountant = True
        return True

    @api.multi
    def cron_expense_to_approve(self):
        acc_day = int(self.env.ref('dba_expense.hr_expense_send_email_accountant').value)
        man_day = int(self.env.ref('dba_expense.hr_expense_send_email_manager').value)
        acc_msg = self.env.ref('dba_expense.message_acc').value
        man_msg = self.env.ref('dba_expense.message_man').value
        today_day = datetime.now().today().day
        admin = self.env['res.users'].browse(self._uid)
        ir_model_data = self.env['ir.model.data']
        res_groups = self.env['res.groups']
        if today_day == acc_day:#Sending email to Accountant
            self._cr.execute('select value from ir_config_parameter where key=%s',('web.base.url',))
            url = str(self._cr.fetchone()[0])
            action_obj = self.env['ir.actions.act_window'].search([('name','=','To be Approve by Accountant'),
                                        ('res_model','=','hr.expense')])
            url+= '/web#view_type=%s&model=%s&action=%s'%('list','hr.expense',action_obj.id)
            self._cr.execute('select id from ir_module_category where name=%s',('DBA AR Modify',))
            category_id = self._cr.fetchone()
            group_id = res_groups.search([('name','=','Accountant'),('category_id','=',category_id[0])])
            email_to = ''
            if group_id:
                for user in group_id[0].users:
                    if user.partner_id.email:
                        email_to = user.partner_id
                        if '@' and '.' not in email_to.email:
                            raise ValidationError(_('Please provide valid email for the Accountant !'))
                        mail_values = {
                                    'subject':'%s Please Approve the Expenses'%(email_to.name),
                                    'author_id':self._uid,
                                    'email_from':admin.partner_id.email or '',
                                    'email_to':email_to.email,
                                    'recipient_ids':email_to,
                                    'reply_to':admin.partner_id.email,
                                    'body_html':str(acc_msg)%(email_to.name,url),
                                }
                        mail_sent = self.env['mail.mail'].create(mail_values).send()
            
        if today_day == man_day:#Sending email to Mamanger
            self._cr.execute('select value from ir_config_parameter where key=%s',('web.base.url',))
            url = str(self._cr.fetchone()[0])
            action_obj = self.env['ir.actions.act_window'].search([('name','=','Expense Reports to Approve'),
                                        ('res_model','=','hr.expense.sheet')])
            url+= '/web#view_type=%s&model=%s&action=%s'%('list','hr.expense.sheet',action_obj[0].id)
            self._cr.execute('select id from ir_module_category where name=%s',('DBA AR Modify',))
            category_id = self._cr.fetchone()
            group_id = res_groups.search([('name','=','Manager'),('category_id','=',category_id[0])])
            email_to = ''
            if group_id:
                for user in group_id[0].users:
                    if user.partner_id.email:
                        email_to = user.partner_id
                        if '@' and '.' not in email_to.email:
                            raise ValidationError(_('Please provide valid email for the Manager !'))
                        mail_values = {
                                    'subject':'%s Please Approve the Expenses'%(email_to.name),
                                    'author_id':self._uid,
                                    'email_from':admin.partner_id.email or '',
                                    'email_to':email_to.email,
                                    'recipient_ids':email_to,
                                    'reply_to':admin.partner_id.email,
                                    'body_html':str(man_msg)%(email_to.name,url),
                                }
                        mail_sent = self.env['mail.mail'].create(mail_values).send()
        return True
class HrExpenseSheetExt(models.Model):
    _inherit = 'hr.expense.sheet'
    pc_no = fields.Char(string='PC#',readonly=True)
    
class HrExpenseRegisterPaymentWizardExt(models.TransientModel):

    _inherit = "hr.expense.register.payment.wizard"
    
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
            #Set PC# in hr.expense.sheet object
            res = expense_sheet.write({'pc_no':self.communication})
        return {'type': 'ir.actions.act_window_close'}
class HrExpenseConfigSettingsExt(models.TransientModel):
    _inherit = 'hr.expense.config.settings'
        
    days = [(days,days) for days in range(1,32)]
    exp_sub_acc = fields.Selection(days,string='Accountant Expense Claim Notification Day of Month',required=True)
    exp_sub_man = fields.Selection(days,string='Manager Expense Claim Notification Day of Month',required=True)
    message_acc = fields.Html('Message For Accountant Expense Email Notification')
    message_man = fields.Html('Message For Manager Expense Email Notification')
    

    @api.model
    def get_default_exp_sub(self, fields):
        acc = int(self.env.ref('dba_expense.hr_expense_send_email_accountant').value)
        man = int(self.env.ref('dba_expense.hr_expense_send_email_manager').value)
        msg_acc = self.env.ref('dba_expense.message_acc').value
        msg_man = self.env.ref('dba_expense.message_man').value
        return {'exp_sub_acc': acc,'exp_sub_man':man,'message_acc':msg_acc,'message_man':msg_man}

    @api.multi
    def set_default_exp_sub(self):
        for record in self:
            self.env.ref('dba_expense.hr_expense_send_email_accountant').write({'value': str(record.exp_sub_acc)})
            self.env.ref('dba_expense.hr_expense_send_email_manager').write({'value': str(record.exp_sub_man)})
            self.env.ref('dba_expense.message_acc').write({'value':str(record.message_acc)})
            self.env.ref('dba_expense.message_man').write({'value':str(record.message_man)})
class product_product(models.Model):
    _inherit = 'product.product'
	
    expense_limit = fields.Float('Expense Limit')

'''class medical_claim_limit(models.Model):
    _name = 'medical.claim.limit'
    
    medical_claim_limit = fields.Float('Medical Claim Limit',required=True)'''
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
