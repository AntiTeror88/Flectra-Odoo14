# -*- coding: utf-8 -*-
# Part of odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleDelivery(models.Model):
    _name = "sale.delivery"
    _description = "Sales Orders Delivery"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    name = fields.Many2one('sale.order','Order Reference', readonly=True)
    date = fields.Datetime('Date Order', readonly=True)
    confirmation_date = fields.Datetime('Confirmation Date', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True)
    product_uom_qty = fields.Float('Qty Ordered', readonly=True)
    qty_delivered = fields.Float('Qty Delivered', readonly=True)
    qty_to_invoice = fields.Float('Qty To Invoice', readonly=True)
    qty_invoiced = fields.Float('Qty Invoiced', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    price_total = fields.Float('Total', readonly=True)
    price_subtotal = fields.Float('Untaxed Total', readonly=True)
    amt_to_invoice = fields.Float('Amount To Invoice', readonly=True)
    amt_invoiced = fields.Float('Amount Invoiced', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product Template', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    nbr = fields.Integer('# of Lines', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)
    team_id = fields.Many2one('crm.team', 'Sales Channel', readonly=True)
    country_id = fields.Many2one('res.country', 'Partner Country', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', 'Commercial Entity', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Sales Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True)
    weight = fields.Float('Gross Weight', readonly=True)
    volume = fields.Float('Volume', readonly=True)
    days_to_confirm = fields.Float('Days To Confirm', readonly=True)
    qty_to_deliver = fields.Float('Qty To Deliver', readonly=True)
    # wh = fields.One2many('stock.picking', string="WH/OUT")

    def init(self):
        """ Sale Delivery """
        tools.drop_view_if_exists(self._cr, 'sale_delivery')
        self._cr.execute(""" CREATE VIEW sale_delivery AS (
            SELECT min(l.id) as id,
                l.product_id as product_id,
                t.uom_id as product_uom,
                sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
                sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
                sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
                sum(l.qty_to_invoice / u.factor * u2.factor) as qty_to_invoice,
                count(*) as nbr,
                s.id as name,
                s.date_order as date,
                s.commitment_date as confirmation_date,
                s.state as state,
                s.partner_id as partner_id,
                s.user_id as user_id,
                s.company_id as company_id,
                extract(epoch from avg(date_trunc('day',s.date_order)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
                t.categ_id as categ_id,
                s.pricelist_id as pricelist_id,
                s.analytic_account_id as analytic_account_id,
                s.team_id as team_id,
                p.product_tmpl_id,
                partner.country_id as country_id,
                partner.commercial_partner_id as commercial_partner_id,
                sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
                sum(p.volume * l.product_uom_qty / u.factor * u2.factor) as volume,
                sum((l.product_uom_qty/u.factor * u2.factor)-(l.qty_delivered/u.factor * u2.factor)) as qty_to_deliver           
            
            FROM
                sale_order_line l
            left join sale_order s on (l.order_id=s.id)
            left join res_partner partner on s.partner_id = partner.id
            left join product_product p on (l.product_id=p.id)
            left join product_template t on (p.product_tmpl_id=t.id)
            left join uom_uom u on (u.id=l.product_uom)
            left join uom_uom u2 on (u2.id=t.uom_id)
            left join product_pricelist pp on (s.pricelist_id = pp.id)
            

            GROUP BY l.product_id,
                    l.order_id,
                    t.uom_id,
                    t.categ_id,
                    s.id,
                    s.date_order,
                    s.commitment_date,
                    s.partner_id,
                    s.user_id,
                    s.state,
                    s.company_id,
                    s.pricelist_id,
                    s.analytic_account_id,
                    s.team_id,
                    p.product_tmpl_id,
                    partner.country_id,
                    partner.commercial_partner_id
        )""")