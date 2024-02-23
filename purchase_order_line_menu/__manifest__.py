# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (https://akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Order Line menu",
    "summary": "Adds a menu to see purchase order lines",
    "version": "13.0.1",
    "author": "Akretion",
    "website": "https://github.com/akretion/odoo-usability",
    "category": "Purchases",
    "depends": [
        "purchase",
        "sale"],
    "data": [
        'views/purchase_order_line.xml',
        'views/sale_order_line.xml',
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
