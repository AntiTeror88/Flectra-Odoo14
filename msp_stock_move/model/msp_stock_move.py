from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp
from odoo.tools import float_round

class StockMove(models.Model):
    _inherit = ['stock.move']
    
    rb= fields.Integer(string=u'RB',store=True)
    rk= fields.Integer(string=u'RK',store=True)
    keterangan_move = fields.Text(string=u'Keterangan',store=True)
