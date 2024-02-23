from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

