# -*- coding: utf-8 -*-
{
    'name': "Field Editor",

    'summary': """
        Field Editor""",

    'description': """
        Field Editor
    """,

    'author': "HashMicro / Janeesh / Vu",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'HashMicro',
    'version': '1.2',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/field_editor_view.xml',
        'views/field_editor_view.xml',
        'views/custom_css_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}