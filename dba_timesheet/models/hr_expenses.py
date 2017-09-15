# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from odoo.tools.translate import _

from datetime import datetime,time
from dateutil.relativedelta import relativedelta
import calendar

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    # display only own expenses for sub admin group
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        if self.env.user.has_group('dba_ar_modify.group_sub_admin_dba'):
        	employee_ids = self.env.user.employee_ids
        	args += [('employee_id','in', self.env.user.employee_ids and self.env.user.employee_ids.ids)]
        return super(HrExpense, self).search(args, offset, limit, order, count=count)