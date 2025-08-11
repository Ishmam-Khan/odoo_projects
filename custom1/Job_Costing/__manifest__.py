{
    'name': 'Job Costing',

    'depends': ['base'],
    'author': 'Ishmam Khan',
    'category': 'Accounting',
    'version': '76.0',
    'summary': 'Manage Job Costing and Balance Sheet',
    'description': 'Module to track job costs and financials in Odoo.',
    'depends': [
         'mail',
         'project',
         'stock',
         'account',
         # 'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        # 'data/sequence.xml',
        # 'views/patient_view.xml',
        # 'views/appointment_views.xml',
        # 'views/appointment_line_views.xml',
        # 'views/patient_tag_view.xml',
        'views/job_costing_views.xml',
        'views/job_type_material_views.xml',
        'views/job_type_views.xml',
        'views/account_job_cost_move_views.xml',
        'views/menu.xml',

        # 'views/patient_action.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}