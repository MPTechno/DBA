# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api
from odoo.tools.translate import _

from datetime import datetime,time
from dateutil.relativedelta import relativedelta
import calendar

class TimeSheetExt(models.Model):
    _inherit = 'hr_timesheet_sheet.sheet'
    
    def action_timesheet_done(self):
        return self.write({'state':'done'})
        
    def cron_remind_timesheet_submission(self):
        user_obj = self.env['res.users']
        users = user_obj.search([])
        day_index = datetime.today().weekday()
        days_list = list(calendar.day_name)
        weekday = days_list[day_index]
        admin = user_obj.browse(self._uid)
        
        if weekday == 'Friday':
            for user in users:
                mail_values = {
                
                    'subject':'Please Fill Timesheet Today',
                    'author_id':self._uid,
                    'email_from':admin.partner_id.email or '',
                    'email_to':user.partner_id.email,
                    'recipient_ids':user.partner_id,
                    'reply_to':admin.partner_id.email,
                    'body_html':'''
                        <h1>Dear %s</h1><br/>
                        <h3>Kindly submit your timesheet by today.</h3><br/>
                        <h4>Thanks</h4>
                    '''%(user.name),
                
                }
                mail_sent = self.env['mail.mail'].create(mail_values).send()
        
        if weekday == 'Monday':
        
            date_to = (datetime.today().date() - relativedelta(days=1)).strftime("%Y-%m-%d")
            date_to = datetime.strptime(date_to,"%Y-%m-%d")
            
            date_from = (date_to - relativedelta(days=6)).strftime("%Y-%m-%d")
            date_from = datetime.strptime(date_from,"%Y-%m-%d")
            
            date_from = str(date_from).split(' ')[0]
            date_to = str(date_to).split(' ')[0]
            
            timesheets_objs = self.search([('date_from','=',date_from),('date_to','=',date_to)])
            timesheet_users = [tobj.employee_id.user_id.id for tobj in timesheets_objs]
            not_submit_ts_users = user_obj.search([('id','not in',timesheet_users)])
            
            for user in not_submit_ts_users:
                related_employee = self.env['hr.employee'].search([('user_id','=',user.id)])
                if len(related_employee):
                    employee = related_employee[0]
                    man_email = employee.parent_id and employee.parent_id.user_id and employee.parent_id.user_id.partner_id.email 
                    mail_values = {
                    
                        'subject':'%s did not submit timesheet'%(user.name),
                        'author_id':self._uid,
                        'email_from':admin.partner_id.email or '',
                        'email_to':user.partner_id.email,
                        'email_cc':man_email,
                        'recipient_ids':user.partner_id,
                        'reply_to':admin.partner_id.email,
                        'body_html':'''
                            <h1>Dear %s</h1><br/>
                            <h3>You did not submited timesheet last week.</h3><br/>
                            <h4>Thanks</h4>
                        '''%(user.name),
                    
                    }
                    mail_sent = self.env['mail.mail'].create(mail_values).send()
        return True
