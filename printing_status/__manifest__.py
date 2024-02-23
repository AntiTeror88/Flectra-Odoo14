{
    'name': 'Printing Status',
    'version': '13.0.0',
    'author': 'Taling Tarung',
    'license': 'OPL-1',
    'category': 'Sales',
    'website': 'https: //www.talingtarung.com/',
    'summary': 'Custom-built Odoo',
    'description': '''
    ''',
    'depends': [
        'account',
        'sale', 
        'purchase',
    ],
    'data': [
        'views/printing_status.xml',
    ],
    'qweb': [
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
