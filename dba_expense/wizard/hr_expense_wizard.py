from odoo import fields, models,api

class ExpenseApplyApproverWizard(models.TransientModel):
    _name = 'expense.apply.approver'
    
    employee_id = fields.Many2one('hr.employee',string="Approver",required=True)
    
    @api.multi
    def set_Approver(self):
        expense_ids = self._context.get('active_ids')
        self.env['hr.expense'].browse(expense_ids).write({'manager_id':self.employee_id.id})
        return True
    
    
