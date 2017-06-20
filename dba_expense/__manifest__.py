# -*- coding: utf-8 -*-
{
    "name": "DBA Expense Customization",
    "author": "HashMicro/ Kunal",
    "version": "10.0.1",
    "website": "www.hashmicro.com",
    "category": "expense",
    "depends": ['base','product','account','hr_expense','document'],
    "data": [
        'security/ir.model.access.csv',
        'data/expense_item_data.xml',
		'views/hr_expense_view.xml',
		'views/expense_report_view.xml',
		'views/invoice_report_view.xml',
    ],
    'description': '''Expense Customization''',
    'demo': [],
    "installable": True,
    "auto_install": False,
}
