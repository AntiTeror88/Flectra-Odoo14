{
    'name': 'Stock Move Delivery',
    'version': '13.0.0',
    'author': 'Taling Tarung',
    'license': 'OPL-1',
    'category': 'Tailor-Made',
    'website': 'https: //www.talingtarung.com/',
    'summary': 'Custom-built Odoo',
    'description': '''
    ''',
    'depends': [
        'stock',
        'product',
        'delivery',
        'base'
    ],
    'data': [
        'report/report_move_delivery.xml',
        # 'security/ir.model.access.csv',
    ],
    'qweb': [
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
