# -*- coding: utf-8 -*-
{
    "name": "Expense Report for Multiple Records",
    "author": "HashMicro/ Kunal",
    "version": "1.0",
    "website": "www.hashmicro.com",
    "category": "expense",
    "depends": ['hr_expense','dba_expense'],
    "data": [
        #'security/ir.model.access.csv',
        'wizard/hr_expense_sheet_report_view.xml',
        'views/expense_sheet_report_template.xml',
    ],
    'description': '''
Features
-------------------
    - This module helps to print the Multiple expense records for the same Employee.
    ''',
    'demo': [],
    "installable": True,
    "auto_install": False,
}
