# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID

class ir_ui_menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        menu_data = [
            'project.menu_main_pm',
            'account.menu_finance_entries',
            'account.menu_finance_reports',
            'stock.menu_stock_root',
            'account.menu_finance_configuration',
        ]
        if self.env.uid != SUPERUSER_ID:
            menu_ids = []
            for menu_item in menu_data:
                menu = self.env.ref(menu_item)
                if menu and menu.id:
                    menu_ids.append(menu.id)
            if menu_ids and len(menu_ids) > 0:
                args.append('!')
                args.append(('id', 'in', menu_ids))
        return super(ir_ui_menu, self).search(args, offset, limit, order, count=count)
