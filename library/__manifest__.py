{
    'name': 'Library Management',
    'version': '1.0.0',
    'author': 'Utsho Biswas',
    "category": 'Human Resources',
    'description': 'Library management system',

    'depends': ['base','product','stock'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/book_borrow_views.xml',
        'views/book_details_views.xml',
        'views/book_genre_views.xml',
        'views/res_partner_views.xml',
        'views/library_menus.xml',
        'views/res_config_settings_views.xml',

    ],
    "demo": [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3'

}


