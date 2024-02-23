from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class StockMoveExtend(models.Model):
    _inherit = 'stock.move.line'

    product_move_tmpl = fields.Many2one(
        'product.template', 'Product Template',
        related='product_id.product_tmpl_id',
        help="Technical: used in views")
    categ_id = fields.Many2one('product.category','Category',related='product_move_tmpl.categ_id', store=True)
    sku = fields.Char(related='product_id.default_code', string='SKU')
    carrier_id = fields.Many2one('delivery.carrier', related='picking_id.carrier_id' , string='Carrier')
    carrier_tracking_ref = fields.Char(related='picking_id.carrier_tracking_ref', string='Tracking Reference')
    partner_id = fields.Many2one('res.partner', related='move_id.partner_id', string='Partner')
    sale_line_id = fields.Many2one('sale.order.line', related='move_id.sale_line_id', string='Sale Line')
    # product_uom_qty = fields.Float(related='sale_line_id.product_uom_qty', string='Order Qty')

class StockMoveExt(models.Model):
    _inherit = 'stock.move'

    categ_id = fields.Many2one('product.category','CategPro',related='product_tmpl_id.categ_id', store=True)

