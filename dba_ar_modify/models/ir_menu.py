# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID

class ir_ui_menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        print "\n\n\n*****current user id",self.env.uid
        menus_for_sub_admin = [
            'account.menu_finance',
            'sale.menu_sale_invoicing',#Sales/Invoicing
            'sales_team.menu_sale_report',#Sales/Reports
            'hr.menu_hr_root',#Employee
            'sale.prod_config_main',#Sales/Configuration/Products
            'sale.menu_product_template_action',#Sales/Sales/Products
            'calendar.mail_menu_calendar',#Calendar
            'mail.mail_channel_menu_root_chat',#Discuss
        ]
        menus_for_sub_admin2 = [
        	'mail.mail_channel_menu_root_chat',#Discuss
        	'calendar.mail_menu_calendar',
        	'utm.menu_link_tracker_root',
            'sales_team.menu_base_partner',
            'account.menu_finance',
            'hr_timesheet.timesheet_menu_root',
            'hr.menu_hr_root',
            'hr_expense.menu_hr_expense_root',
            'base.menu_management',
            'base.menu_administration',
            'calendar.mail_menu_calendar',#Calendar
        ]
        menus_for_user = [
            'mail.mail_channel_menu_root_chat',#Discuss
        	'calendar.mail_menu_calendar',
        	'utm.menu_link_tracker_root',
            'sales_team.menu_base_partner',
            'dba_ar_modify.menu_sales_project_code',
            'account.menu_finance',
            'hr_timesheet.timesheet_menu_root',
            'hr.menu_hr_root',
            'hr_expense.menu_hr_expense_root',
            'base.menu_management',
            'base.menu_administration',
            'calendar.mail_menu_calendar',#Calendar
        ]
        menus_for_manager = [
            'mail.mail_channel_menu_root_chat',
        	'calendar.mail_menu_calendar',
        	'utm.menu_link_tracker_root',
            'sales_team.menu_base_partner',
            'account.menu_finance',
            'hr_timesheet.timesheet_menu_root',
            'hr.menu_hr_root',
            'hr_expense.menu_hr_expense_root',
            'base.menu_management',
            'base.menu_administration',
            'calendar.mail_menu_calendar',#Calendar
            'mail.mail_channel_menu_root_chat',#Discuss
        ]
        dba_user_id = self.env['ir.model.data'].get_object_reference('dba_ar_modify', 'group_user_dba')[1]
        dba_manager_id = self.env['ir.model.data'].get_object_reference('dba_ar_modify', 'group_manager_dba')[1]
        sub_admin_id = self.env['ir.model.data'].get_object_reference('dba_ar_modify', 'group_sub_admin_dba')[1]
        sub_admin2_id = self.env['ir.model.data'].get_object_reference('dba_ar_modify', 'group_sub_admin2_dba')[1]
        print"\nsub_admin2_id",sub_admin2_id
        for group in self.env['res.users'].browse(self.env.uid).groups_id:
            if group.id == dba_user_id:
            	print"111"
                menu_ids = []
                for menu_item in menus_for_user:
                    menu = self.env.ref(menu_item)
                    if menu and menu.id:
                        menu_ids.append(menu.id)
                if menu_ids and len(menu_ids) > 0:
                    args.append('!')
                    args.append(('id', 'in', menu_ids))
            if group.id == dba_manager_id:
            	print"222"
                menu_ids = []
                for menu_item in menus_for_manager:
                    menu = self.env.ref(menu_item)
                    if menu and menu.id:
                        menu_ids.append(menu.id)
                if menu_ids and len(menu_ids) > 0:
                    args.append('!')
                    args.append(('id', 'in', menu_ids))
            if group.id == sub_admin_id:
            	print"333"
                menu_ids = []
                for menu_item in menus_for_sub_admin:
                    menu = self.env.ref(menu_item)
                    if menu and menu.id:
                        menu_ids.append(menu.id)
                if menu_ids and len(menu_ids) > 0:
                    args.append('!')
                    args.append(('id', 'in', menu_ids))
            if group.id == sub_admin2_id:
                print"444"
                menu_ids = []
                for menu_item in menus_for_sub_admin2:
                    menu = self.env.ref(menu_item)
                    if menu and menu.id:
                        menu_ids.append(menu.id)
                if menu_ids and len(menu_ids) > 0:
                    args.append('!')
                    args.append(('id', 'in', menu_ids))
        menu_data = [
            'purchase.menu_purchase_root',
        ]
        if self.env.uid != SUPERUSER_ID or 1 == 1:
            menu_ids = []
            for menu_item in menu_data:
                menu = self.env.ref(menu_item)
                if menu and menu.id:
                    menu_ids.append(menu.id)
            if menu_ids and len(menu_ids) > 0:
                args.append('!')
                args.append(('id', 'in', menu_ids))
        return super(ir_ui_menu, self).search(args, offset, limit, order, count=count)
