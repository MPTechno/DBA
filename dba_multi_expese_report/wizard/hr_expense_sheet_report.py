from odoo import fields, models

class ExpenseSheetReport(models.TransientModel):
    _name = 'expense.sheet.report'
    

    def _build_contexts(self, data):
        result = {}
        return result

    def print_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        used_context = self._build_contexts(data)#p
        return self.env['report'].get_action(self, 'dba_multi_expese_report.expense_sheet_report',data=data)
    
    
