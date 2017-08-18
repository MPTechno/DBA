{
    "name": "DBA Access Rights Modify",
    "version": "1.0",
    "depends": ["sale",
                "stock",
                "crm",
                "analytic",
                "account",
                "project",
                "hr_expense",
                "stock_account",
                "project_issue_sheet",
                "hr_timesheet_invoice",
                "hr_timesheet_sheet",
                ],
    "author": "Hashmicro/Kunal",
    "website": "http://www.hashmicro.com",
    "category": "dba",
    'sequence': 1,
    "description": """
Create some access right ID group.
-------------------------------------
    - Admin As an administrator.
    - Sub Admin
    - Sub Admin-2
    - Manager
    - Accountant As an administrator
    - User
""",
    'data': [
        'security/group_data.xml',
        'security/ir.model.access.csv',
        'views/new_menus.xml',
    ],
    'installable': True,
    'active': False,
    'auto_install': False,
    'application': True,
}
