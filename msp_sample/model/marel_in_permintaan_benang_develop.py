from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class MarelinPermintaanBenangdevelopLine(models.Model):
    _name = 'marelin.permintaan.benang.developline'
    
    # relasi untuk one2many
    
    permintaan_benang_develop_id = fields.Many2one('marelin.permintaan.develop',string=u'Nama Desain Id',)
    # fields untuk ambil data nama desain
    product_id = fields.Many2one('product.product',string=u'Nama Benang',)
    jmlh_ambil_kg = fields.Float(string=u'Jumlah Ambil Kg',)
    jmlh_ambil_connes = fields.Float(string=u'Jumlah Ambil Connes',)
    jmlh_sisa_kg = fields.Float(string=u'Jumlah Sisa Kg',)
    jmlh_sisa_connes = fields.Float(string=u'Jumlah Sisa Connes',)
    keterangan = fields.Text(string=u'Keterangan',)
    partner_id = fields.Many2one('res.partner', string='Customer',)
    

class MarelInPermintaanBenangDevelop(models.Model):
    _name = 'marelin.permintaan.develop'
    # _rec_name = 'nama_desain_sample'    
    # penghubung fields many2one permintaan.benang.sample.list

    def get_marel_in_permintaan_benang_develop_no(self):
        nama_baru = self.env['ir.sequence'].next_by_code('marelin.permintaan.develop.no')
        return nama_baru
      
    name = fields.Char(string='No Id',required=True,copy=False, default=get_marel_in_permintaan_benang_develop_no,readonly=True )

    marelin_permintaan_benang_developline_ids = fields.One2many('marelin.permintaan.benang.developline','permintaan_benang_develop_id',string=u'Permintaan Benang Develop',)
    tgl = fields.Date(string=u'Tanggal',default=fields.Date.context_today,readonly=True,)
    needle = fields.Char(string=u'Needle',)
    nama_desain_develop = fields.Char(string=u'Nama Desain',required=True,)
    partner_id = fields.Many2one('res.partner', string='Customer',)