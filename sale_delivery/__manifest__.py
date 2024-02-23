# -*- coding: utf-8 -*-
# Part of odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Sale Delivery",
    'version': "1.0",
    'category': "Sales",
    'summary': "Outstanding Sale Delivery",
    'description': """
Outstanding delivery
    """,
    'depends': ['sale','purchase','base', 'sale_stock'],
    'data': [
        'report/sale_delivery_report.xml',
        'report/purchase_delivery_report.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}