# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime

class AccountJournal(models.Model):
    _inherit = 'account.journal'
	
    @api.multi
    @api.depends('name', 'currency_id', 'company_id', 'company_id.currency_id')
    def name_get(self):
        res = []
        for journal in self:
            currency = journal.currency_id or journal.company_id.currency_id
            name = "%s" % (journal.name)
            res += [(journal.id, name)]
        return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
