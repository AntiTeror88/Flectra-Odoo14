{
   'name': 'Stock Vendor In Lot',
   'version': '14.0.0',
   'author': 'Taling Tarung',
   'license': 'OPL-1',
   'category': 'Tailor-Made',
   'website': 'https: //www.talingtarung.com/',
   'summary': 'Custom-built Odoo',
   'description': '''
   Custom add vendor in lot
   ''',
   'depends': [
       'stock',
       'product',
       'base',
   ],
   'data': [
       'views/vendor_in_lot.xml',
       'views/stock_move_view.xml',
       'views/stock_quant_view.xml',
   ],
   'qweb': [
   ],
   'auto_install': False,
   'installable': True,
   'application': True,
}