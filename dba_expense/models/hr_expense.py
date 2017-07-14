# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime

class hr_expense(models.Model):
    _inherit = 'hr.expense'
	
    paid_by = fields.Selection([('Cash','Cash'),('Cheque','Cheque')],'Paid By', default='Cash')
    cheque_no = fields.Char('Cheque No')
    pc_no = fields.Char('PC#')
    manager_id = fields.Many2one('hr.employee','Approver')
    
    
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
        if self.product_id.expense_limit != 0.0 and self.total_amount > self.product_id.expense_limit:
            raise UserError(_("You can't add more expense than %s !") % (self.product_id.expense_limit))
        if any(expense.state != 'draft' for expense in self):
            raise UserError(_("You cannot report twice the same line!"))
        if len(self.mapped('employee_id')) != 1:
            raise UserError(_("You cannot report expenses for different employees in the same report!"))
        if not self.manager_id:
            raise ValidationError(_('Please Selet the Manager to Approve !'))
        ir_model_data = self.env['ir.model.data']
        email_to = ''
        if self.manager_id:
            if self.manager_id.user_id:
                email_to = str(self.manager_id.user_id.partner_id.email)
        if '@' and '.' not in email_to:
            raise ValidationError(_('Please provide valid email for the Manager !'))
        self.ensure_one()
        template_id = ir_model_data.get_object_reference('dba_expense', 'expense_claim_email_template')[1]
        if template_id:
            self.env['mail.template'].browse(template_id).send_mail(self.id)
        mail_mail_ids = self.env['mail.mail'].search([('state','=','outgoing')])
        if mail_mail_ids:
            for mail_mail_id in mail_mail_ids:
                mail_mail_id.write({'email_to':email_to})
                mail_mail_id.send()
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
            expense.total_amount = self.unit_amount * expense.quantity
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
        ir_model_data = self.env['ir.model.data']
        res_groups = self.env['res.groups']
        self._cr.execute('select id from ir_module_category where name=%s',('DBA AR Modify',))
        category_id = self._cr.fetchone()
        group_id = res_groups.search([('name','=','Accountant'),('category_id','=',category_id[0])])
        email_to = ''
        if group_id:
            for user in group_id[0].users:
                if user.partner_id.email:
                    email_to = email_to + str(user.partner_id.email) +','
        if '@' and '.' not in email_to:
            raise ValidationError(_('Please provide valid email for the Accountant !'))
        self.ensure_one()
        template_id = ir_model_data.get_object_reference('dba_expense', 'expense_claim_email_template')[1]
        if template_id:
            self.env['mail.template'].browse(template_id).send_mail(self.id)
        mail_mail_ids = self.env['mail.mail'].search([('state','=','outgoing')])
        if mail_mail_ids:
            for mail_mail_id in mail_mail_ids:
                mail_mail_id.write({'email_to':email_to})
                mail_mail_id.send()
        return True
    
    def _check_date(self):
        if self.date:
            today_date = datetime.now().date()
            current_date = datetime.strptime(str(today_date), '%Y-%m-%d').date()
            expense_date = datetime.strptime(self.date, '%Y-%m-%d').date()
            month = (current_date.year - expense_date.year) * 12 + current_date.month - expense_date.month
            if month >= 3:
                raise ValidationError(_('Expense Date is 3 months more than the Current Date !'))
    @api.multi
    def get_access_action(self):
        self.ensure_one()
        res = super(hr_expense, self).get_access_action()
        self._cr.execute('select value from ir_config_parameter where key=%s',('web.base.url',))
        url = str(self._cr.fetchone()[0])
        if url:
            url+= '/web#id=%s&view_type=%s&model=%s&action=%s'%(
                                                             res.get('res_id'),
                                                             res.get('view_type'),
                                                             res.get('res_model'),
                                                             res['context']['params']['action'])
            return {'url':url}
        return res
class product_product(models.Model):
    _inherit = 'product.product'
	
    expense_limit = fields.Float('Expense Limit')

'''class medical_claim_limit(models.Model):
    _name = 'medical.claim.limit'
    
    medical_claim_limit = fields.Float('Medical Claim Limit',required=True)'''
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
