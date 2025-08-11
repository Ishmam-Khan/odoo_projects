# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real-Estate-Management',

    'depends': ['base'],
    'author': 'Mir Info System',
    'category': 'Real Estate',
    'version': '6.0',
    'summary': 'Manage properties, buyers, and transactions',
    'description': 'A module to manage Real estate properties in Odoo',
    'data': [

        'views/customer_views.xml',
        'views/menu.xml',


    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
