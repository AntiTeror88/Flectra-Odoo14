# -*- coding: utf-8 -*-
# Copyright 2018 Raphael Reverdy https://akretion.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    po_name = fields.Char(string="Order", related='order_id.name', store=True)
    product_template_id = fields.Many2one('product.template', string='Product Template',related='product_id.product_tmpl_id')
    categ_id = fields.Many2one('product.category', string='Product Category', related='product_template_id.categ_id', store=True)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    pass