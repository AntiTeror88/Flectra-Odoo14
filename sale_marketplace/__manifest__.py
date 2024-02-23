{
    'name': 'Sale Market Place',
    'version': '13.0.0',
    'author': 'Taling Tarung',
    'license': 'OPL-1',
    'category': 'Tailor-Made',
    'website': 'https: //www.talingtarung.com/',
    'summary': 'Custom-built Odoo',
    'description': '''Add Market Place Reference
    ''',
    'depends': [
        'account', # python
        'sale', # python
    ],
    'data': [
        'views/market_place.xml',
        'views/sale_marketplace.xml',
        'security/ir.model.access.csv',
        'reports/account_invoice_report_view.xml',
        'reports/sale_report_view.xml',
    ],
    'qweb': [
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
