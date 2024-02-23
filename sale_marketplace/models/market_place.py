from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

class MarketPlace(models.Model):
    _name = "market.place"
    _description = "Market Place"

    name = fields.Char(string='Name', required=True)
    ref = fields.Char(string='Reference')
    no_account = fields.Char(string='No Account')
    renewal = fields.Date(string='Tgl Renewal')
