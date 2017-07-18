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
        notification_obj = self.env['timesheet.notification.config']
        notification = notification_obj.search([])
        day_index = datetime.today().weekday()
        days_list = list(calendar.day_name)
        weekday = days_list[day_index]
        admin = user_obj.browse(self._uid)
        if notification:
            if weekday == str(notification.reminder_day):
                timesheets_objs = self.search([('state','=','draft')])
                timesheet_emps = [tobj.employee_id for tobj in timesheets_objs]
                for emp in timesheet_emps:
                    mail_values = {
                        'subject':'Please Fill Timesheet Today',
                        'author_id':self._uid,
                        'email_from':admin.partner_id.email or '',
                        'email_to':emp.user_id.partner_id.email,
                        'recipient_ids':emp.user_id.partner_id,
                        'reply_to':admin.partner_id.email,
                        'body_html':str(notification.reminder_message)%(emp.name,emp.parent_id.name),
                    }
                    mail_sent = self.env['mail.mail'].create(mail_values).send()
            
            if weekday == str(notification.notify_day):
                date_to = (datetime.today().date() - relativedelta(days=1)).strftime("%Y-%m-%d")
                date_to = datetime.strptime(date_to,"%Y-%m-%d")
                
                date_from = (date_to - relativedelta(days=6)).strftime("%Y-%m-%d")
                date_from = datetime.strptime(date_from,"%Y-%m-%d")
                
                date_from = str(date_from).split(' ')[0]
                date_to = str(date_to).split(' ')[0]
                timesheets_objs = self.search([('date_from','=',date_from),('date_to','=',date_to),('state','=','draft')])
                timesheet_emps = [tobj.employee_id for tobj in timesheets_objs]
                for emp in timesheet_emps:
                    man_email = emp.parent_id and emp.parent_id.user_id and emp.parent_id.user_id.partner_id.email or ''
                    mail_values = {
                        'subject':'%s did not submit timesheet'%(emp.name),
                        'author_id':self._uid,
                        'email_from':admin.partner_id.email or '',
                        'email_to':user.partner_id.email,
                        'email_cc':man_email,
                        'recipient_ids':emp.user_id.partner_id,
                        'reply_to':admin.partner_id.email,
                        'body_html':str(notification.notify_message)%(emp.name,emp.parent_id.name),
                    }
                    mail_sent = self.env['mail.mail'].create(mail_values).send()
        return True
        
class TimesheetNotificationConfig(models.Model):
    _name = 'timesheet.notification.config'
    
    def _get_reminder_msg(self):
        msg = '''Dear %s,<br/>'''
        msg += '''You forgot to submit your timesheet this week <br/>'''
        msg += '''Regards,'''
        return msg
    def _get_notify_msg(self):
        msg = '''Dear %s,<br/>'''
        msg += '''This is second notify<br/>'''
        msg += '''you forgot to submit your timesheet last week<br/>'''
        msg += '''Regards,'''
        return msg
    
    reminder_day = fields.Char(string="Reminder Day",required=True)
    notify_day = fields.Char(string="Notificaton Day",required=True)
    reminder_message = fields.Html(string="Reminder Message",required=True,default=_get_reminder_msg)
    notify_message = fields.Html(string="Notification Message",required=True,default=_get_notify_msg)
    
    _rec_name = 'reminder_day'
