# -*- coding: utf-8 -*-
{
    "name": "DBA Expense Customization",
    "author": "HashMicro/ Kunal",
    "version": "10.0.1",
    "website": "www.hashmicro.com",
    "category": "expense",
    "depends": ['base','product','account','hr_expense','document','dba_ar_modify'],
    "data": [
        'security/ir.model.access.csv',
        'data/expense_item_data.xml',
        'data/mail_template_data.xml',
		'views/hr_expense_view.xml',
		'views/expense_report_view.xml',
		'views/invoice_report_view.xml',
    ],
    'description': '''
Features
-------------------
    - Accountant and Manager
        a. When an employee click “Submit to Accountant” for expense claim.
            An email will send to accountant email which contains the link of expense to get an
            approval.
        b. Accountant will check and able to see “Submit to Manager” button to approve the expense
            (Status change to “Submitted”) and send an email notify to Manager for approval which
            contain the link of expense.
            Once Manager approve, the Status change to “Approved”
    ''',
    'demo': [],
    "installable": True,
    "auto_install": False,
}
