from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class Picking(models.Model):

    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        res = super(Picking, self.with_context(mail_create_nosubscribe=True)).create(vals)
        if vals.get('partner_id'):
            for picking in res.filtered(lambda p: p.location_id.usage == 'supplier' or p.location_dest_id.usage == 'customer'):
                picking.message_unsubscribe([vals.get('partner_id')])
        return res

    def write(self, vals):
        res = super(Picking, self.with_context(mail_create_nosubscribe=True)).write(vals)
        if vals.get('partner_id'):
            for picking in self:
                if picking.location_id.usage == 'supplier' or picking.location_dest_id.usage == 'customer':
                    if picking.partner_id:
                        picking.message_unsubscribe(picking.partner_id.ids)
                    picking.message_unsubscribe([vals.get('partner_id')])
        return res

    def button_validate(self):
        for picking in self:
            picking.message_unsubscribe([self.env.user.partner_id.id])
        return super(Picking, self).button_validate()