# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    date_order = fields.Datetime(string='Order Date', related='order_id.date_order', store=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    pass