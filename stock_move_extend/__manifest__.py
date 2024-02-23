# -*- coding: utf-8 -*-
# Part of Odoo, odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Moves Extent Search',
    'author': 'Art-In-Heaven',
    'version': '13.0',
    'summary': 'Inventory, Logistics, Warehousing',
    'description': "",
    'website': "https://gitlab.com/art-in-heaven",
    'depends': ['base',
                'stock',
                'product',
                'delivery',
                'account',
                ],
    'category': 'Warehouse',
    'data': [
        'views/stock_move_extend_view.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}
