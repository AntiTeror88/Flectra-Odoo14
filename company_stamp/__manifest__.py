# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Company Stamp",
    "version": "1.0.1.2.0",
    "author": "odoo Community, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "summary": 'Stamp',
    "category": "",
    "depends": [
        'web',
        'base',
        'account',
        'purchase',
        'sale',
    ],
    "data": [
        "views/company_stamp.xml",
    ],

    "installable": True,
}