from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp
from odoo.tools import float_round

class MarelInStockPicking(models.Model):
    _inherit = ['stock.picking']
    
    no_mo_id = fields.Many2one('mrp.production',string='No Mo')
    no_SO = fields.Char(related='no_mo_id.origin',string='No SO', readonly=True)
    status = fields.Selection(string=u'Status',selection=[('Cukup', 'Cukup'), ('Kurang', 'Kurang')])    
    
    no_bpb = fields.Char(string='No BPB',index=True, copy=False, default=lambda x: _('/'))
    no_spb = fields.Char(string='No SPB',index=True, copy=False, default=lambda x: _('/'))
    nama_pengemudi = fields.Char(string='Nama Pengemudi')
    no_plat_truck = fields.Char(string='No Plat Truck')
    tgl_transaksi = fields.Date(string='Tgl Transaksi',default=fields.Date.context_today,store=True)
    no_sj = fields.Char(string='No SJ',index=True, copy=False, default=lambda x: _('/'))
    no_sj_supplier = fields.Char(string='No SJ supplier')
    partner_id = fields.Many2one('res.partner', 'Partner',states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    tgl_keluar = fields.Date(string='Tgl Keluar (Spr)',default=fields.Date.context_today,store=True)
    tgl_kirim = fields.Date(string='Tgl Kirim (Spr)',default=fields.Date.context_today,store=True)
    
    sj_report = fields.Boolean(string='Print SJ',)
    bpb_report = fields.Boolean(string='Print BPB',)
    spb_report = fields.Boolean(string='Print SPB',)
    

    def button_sj_no(self):
        if not self.no_sj or self.no_sj == _('/'):
            self.no_sj = self.env['ir.sequence'].next_by_code('marel.sj.no') or _('/')

    def button_bpb_no(self):
        if not self.no_bpb or self.no_bpb == _('/'):
            self.no_bpb = self.env['ir.sequence'].next_by_code('marel.bpb.no') or _('/')
    
    def button_spb_no(self):
        if not self.no_spb or self.no_spb == _('/'):
            self.no_spb = self.env['ir.sequence'].next_by_code('marel.spb.no') or _('/')