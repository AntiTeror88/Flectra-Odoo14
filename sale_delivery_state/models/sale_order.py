from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    # whname = fields.One2many('Del Reference', compute="_delivery_list")
    whstate = fields.Char('Del Status', compute="_delivery_list")
    # invno = fields.Char('Inv No', compute="_inv_no")
    payment = fields.Char('Paid', compute="_inv_no")


    def _delivery_list(self):
        for i in self:
            if i.picking_ids:
                for n in i.picking_ids:
                    picks = self.env['stock.picking'].search([('id','=',n.id)], order='id desc', limit=1)[-1]
                    i.whstate = picks.state
            else:
                i.whstate = 'no delivery'

    def _inv_no(self):
        for i in self:
            if i.invoice_ids:
                for n in i.invoice_ids:
                    inv = self.env['account.move'].search([('id','=',n.id)], order='id desc', limit=1)[-1]
                    i.payment = n.invoice_payment_state
            else:
                i.payment = 'no invoice'
        
            