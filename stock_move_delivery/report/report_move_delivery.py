# -*- coding: utf-8 -*-
from odoo import models, fields, tools, api


class ReportMoveDelivery (models.Model):
    _name = 'report.move.delivery'
    _description = 'Product Move Delivery'

    datedelivered = fields.Date (string='Date', readonly=True)
    sku = fields.Many2one ('product.product', string='SKU', readonly=True)
    description = fields.Many2one ('product.template', string='Description', readonly=True)
    qty_del = fields.Integer (string='Qty', readonly=True)
    # sj_no = fields.Char (string='No WH', readonly=True)
    # carrier = fields.Char (string='Kurir', readonly=True)
    # so_no = fields.Char (string='SO', readonly=True)
    # state = fields.Char (string='State', readonly=True)
    # code = fields.Many2one ('stock.picking.type', string='code', readonly=True)

    def init(self):
        """ Stock Move Delivery """
        tools.drop_view_if_exists(self.env.cr, 'report_move_delivery')
        self.env.cr.execute(""" CREATE VIEW report_move_delivery AS (
            SELECT
                l.id,
                l.date_done as datedelivered,
                pp.default_code as sku, 
                pt.name as description, 
                l.qty_done as qty_del,
                # p.name as sj_no, 
                # dc.name as carrier, 
                # m.origin as so_no,
                # m.state as state,
                # spt.code as code
            FROM 
                stock_move_line l
            # LEFT JOIN 
            #     stock_move m ON m.id=l.move_id
            # LEFT JOIN 
            #     stock_picking p ON p.id=l.picking_id
            # LEFT JOIN 
            #     delivery_carrier dc ON dc.id=p.carrier_id
            # LEFT JOIN
            #     stock_picking_type spt ON spt.id=p.picking_type_id
            LEFT JOIN 
                product_product pp ON pp.id=l.product_id
            LEFT JOIN 
                product_template pt ON pt.id=pp.product_tmpl_id
            LEFT JOIN 
                product_category pc ON pc.id=pt.categ_id

        )""")
       