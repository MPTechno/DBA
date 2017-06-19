# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api

class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    journal_id = fields.Many2one('account.journal', 'Journal', compute='_compute_journal_id', store=True)

    @api.depends('move_id', 'move_id.journal_id')
    def _compute_journal_id(self):
        for ts_line in self:
            if ts_line.move_id and ts_line.move_id.journal_id:
                ts_line.journal_id = ts_line.move_id.journal_id.id
            else:
                # Timesheet Journal
                if ts_line.sheet_id and ts_line.sheet_id.id:
                    timesheet_journal = self.env.ref('hr_timesheet_invoice.timesheet_journal')
                    if timesheet_journal and timesheet_journal.id:
                        ts_line.journal_id = timesheet_journal.id
                    else:
                        ts_line.journal_id = False
                else:
                    ts_line.journal_id = False

    @api.depends('date', 'user_id', 'project_id', 'account_id', 'sheet_id_computed.date_to', 'sheet_id_computed.date_from', 'sheet_id_computed.employee_id')
    def _compute_sheet(self):
        """Links the timesheet line to the corresponding sheet
        """
        for ts_line in self:
            # TODO: Disable project_id
            # if not ts_line.project_id:
            #     continue
            if ts_line.product_id:
                continue
            sheets = self.env['hr_timesheet_sheet.sheet'].search(
                [('date_to', '>=', ts_line.date), ('date_from', '<=', ts_line.date),
                 ('employee_id.user_id.id', '=', ts_line.user_id.id),
                 ('state', 'in', ['draft', 'new'])])
            if sheets:
                # [0] because only one sheet possible for an employee between 2 dates
                ts_line.sheet_id_computed = sheets[0]
                ts_line.sheet_id = sheets[0]