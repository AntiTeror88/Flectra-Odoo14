# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    price_caltotal = fields.Monetary(compute='_compute_calamount', string='Caltotal', readonly=True, store=True)

    @api.depends('product_uom_qty', 'discount', 'price_unit')
    def _compute_calamount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            caltotal = line.product_uom_qty * price
            line.update({
                'price_caltotal': (caltotal)
            })

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res['is_delivery']= self.is_delivery
        return res

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    price_caltotal = fields.Monetary(compute='_compute_calamount', string='Caltotal', readonly=True, store=True)

    @api.depends('product_uom_qty', 'discount', 'price_unit')
    def _compute_calamount(self):
        """
        Compute the amounts of the PO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            caltotal = line.product_uom_qty * price
            line.update({
                'price_caltotal': (caltotal)
            })

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    price_caltotal = fields.Monetary(compute='_compute_calamount', string='Caltotal', readonly=True, store=True)
    is_delivery = fields.Boolean(string="Line Delivery", default=False)

    @api.depends('quantity', 'discount', 'price_unit')
    def _compute_calamount(self):
        
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            caltotal = line.quantity * price
            line.update({
                'price_caltotal': (caltotal)
            })


    

    