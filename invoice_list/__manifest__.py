{
    'name': 'Invoice List',
    'version': '14.1.0',
    'author': 'Taling Tarung',
    'license': 'OPL-1',
    'category': 'Invoicing',
    'website': 'https: //www.talingtarung.com/',
    'summary': 'Custom-built odoo',
    'description': '''
    ''',
    'depends': [
        'base', 
        'account', 
        'sale',
        'stock',
        'product',
    ],
    'data': [
        'views/invoice_list_menu.xml',
        'report/invoice_list.xml',
        # 'report/invoice_perform.xml',
        # 'security/ir.model.access.csv',
    ],
    'qweb': [
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}