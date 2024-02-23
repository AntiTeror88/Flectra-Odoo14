from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round

class MarelInPurchase(models.Model):
    _inherit = ['purchase.order']
    
    no_pajak = fields.Char(string='No/Faktur Pajak',)
    surat_jalan = fields.Char(string='Surat Jalan',)
    kurs = fields.Float(string=u'Jumlah Kurs',store=True)
    jenis_kurs = fields.Selection(string=u'Jenis Kurs',selection=[('kurs_tengah_bi', 'Kurs Tengah BI'), ('kurs_pajak', 'Kurs Pajak'), ('kurs_averydennison', 'Kurs Averydennison')])
    scheduled_date = fields.Date(string='Scheduled Date',default=fields.Date.context_today,store=True)
    taxes_id = fields.Char(string='Taxes',related='order_line.taxes_id.name', )
    po_local = fields.Boolean(string='PO Local',store=True)
    po_import = fields.Boolean(string='PO Import',store=True)


class MarelInPurchaseLine(models.Model):
    _inherit = ['purchase.order.line']
    
    status = fields.Selection(string=u'Status',selection=[('Celup', 'Celup'), ('Beli', 'Beli'), ('Maklon', 'Maklon')], store=True)
    kurs = fields.Float(string=u'Kurs', store=True)
    keterangan = fields.Text(string=u'Keterangan', store=True)
    harga_dolar = fields.Float(string=u'Hrga USD',digits=dp.get_precision('Custom 1'),default=1.0, store=True)
    ket_gramasi = fields.Boolean(string=u'Kurs ?', store=True)
    standard_price_product = fields.Float(string=u'Hrga USD',related='product_id.standard_price',readonly=True,store=True )

    @api.onchange('ket_gramasi')
    def get_purchase_menggunakan_kurs(self):
        if self.ket_gramasi:
            self.price_unit = (self.order_id.kurs * self.harga_dolar)
        return
