# -*- coding: utf-8 -*-
import time
from odoo import fields, models, exceptions, api
from odoo.tools.translate import _

class TimeSheetExt(models.Model):
    _inherit = 'hr_timesheet_sheet.sheet'
    
    def action_timesheet_done(self):
        return self.write({'state':'done'})
