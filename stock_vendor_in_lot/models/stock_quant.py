# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    vendor_id = fields.Many2one(related='lot_id.vendor_id', store=True, readonly=True)