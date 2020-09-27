# -*- coding: utf-8 -*-
{
    'name': "abvo",

    'summary': """
        Add Certificates to ABVO Website""",

    'description': """
        Add Certificates to ABVO Website
    """,

    'author': "POPSOLUTIONS.CO",
    'website': "https://www.popsolutions.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'sale',
                'portal',
                'contacts',
                'membership',
                'website_membership'],

    # always loaded
    'data': [
        'security/abvo_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_partner_view.xml',
        'views/abvo_certificates_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}