# -*- coding: utf-8 -*-
{
    "name": "DBA Timesheet Customization",
    "author": "HashMicro/ Kunal",
    "version": "1.0",
    "website": "www.hashmicro.com",
    "category": "timesheet",
    "depends": ['hr_timesheet_sheet','hr_timesheet_invoice'],
    "data": [
        'security/security.xml',
		'views/timesheet_view.xml',
		'data/cron.xml',
    ],
    'description': '''
Features
--------
    - User and Manager
        a. Every Friday(Morning 00:00 am, Emails),User is able to receive Email notifications as a
            Reminder for not submitting the Timesheet by Friday of every week.
        b. Both Manager and User are able to receive Email Notifications on Monday of every week,
            stating that the particular User has not Submitted the ‘Timesheet’.
            Condition : If User has not submitted the timesheet by Friday of every week.
        c. User is able to configure the Notifications for the Timesheet .    
    ''',
    'demo': [],
    'installable': True,
    'auto_install': False,
}
