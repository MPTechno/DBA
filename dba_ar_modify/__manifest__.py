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
    - Manager
    - Accountant
    - User
""",
    'data': [
        'security/group_data.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'active': False,
    'auto_install': False,
    'application': True,
}
