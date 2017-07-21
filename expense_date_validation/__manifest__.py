# -*- coding: utf-8 -*-
{
    "name": "Expense Date Validation",
    "author": "HashMicro/ Kunal",
    "version": "10.0.1",
    "website": "www.hashmicro.com",
    "category": "expense",
    "depends": ['hr_expense'],
    "data": [
        'views/expense_time_limit_view.xml',
        'data/expense_submit_limit_data.xml',
    ],
    'description': '''
Features
-------------------
    - More than 3 month's of expense date then user can not apply
    ''',
    'demo': [],
    "installable": True,
    "auto_install": False,
}
