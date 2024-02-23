# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StockMove(models.Model):
   _inherit = 'stock.move'

   vendor_id = fields.Many2one('res.partner', 'Vendor')