{
    'name': 'Sale Order Delivery State',
    'version': '13.0.0',
    'author': 'Taling Tarung',
    'license': 'OPL-1',
    'category': 'Tailor-Made',
    'website': 'https: //www.talingtarung.com/',
    'summary': 'Custom-built Odoo',
    'description': '''
    ''',
    'depends': [
        'account',
        'sale',
        'stock',
        'product',
        'sale_stock',
        'base',
        'account_payment',
    ],
    'data': [
        # 'report/sale_delivery_state.xml',
        'views/sale_order.xml',
    ],
    'qweb': [
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}