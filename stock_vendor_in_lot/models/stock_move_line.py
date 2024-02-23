# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    vendor_id = fields.Many2one('res.partner', 'Vendor')

    # @api.onchange('lot_id')
    # def _onchange_lot_id(self):
    #     if self.lot_id.vendor_id and self.picking_id.picking_type_id.id == 1:
    #         self.vendor_id = self.lot_id.vendor_id
    #     else:
    #         self.vendor_id = False

    def write(self, vals):
        res= super(StockMoveLine, self).write(vals)
        if 'vendor_id' and not self.lot_id.vendor_id and self.picking_id.picking_type_id.id == 1:
            for val in self:
                self.env['stock.production.lot'].search([('id', '=', val.lot_id.id)]).write({'vendor_id' : val.vendor_id.id})
            return res
        