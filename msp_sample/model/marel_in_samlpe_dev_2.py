from odoo.addons import decimal_precision as dp
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.tools import float_round

class MspSampleDevLine(models.Model):
    _name = 'msp.sample.dev.line'

    msp_sample_dev_id = fields.Many2one('msp.sample.dev',string=u'marel in samlpe_dev id',)
    #------------
    product_id = fields.Many2one('product.product',string=u'Nama Benang',)
    jumlah_ambil = fields.Float(string=u'Jmlah Ambil (C)',)
    qty_benang_kg = fields.Float(string=u'Qty Benang Per Pasang (kg)',digits=dp.get_precision('Custom 2'),)
    qty_benang_gr = fields.Float(string=u'Qty Benang Per Pasang (gr)',digits=dp.get_precision('Custom 2'),)
    qty_bom_reguler = fields.Float(string=u'Qty Bom (R)',digits=dp.get_precision('Custom 2'),)
    qty_bom_soccer = fields.Float(string=u'Qty Bom (S)',digits=dp.get_precision('Custom 2'),)
    partner_id = fields.Many2one('res.partner', string='Customer', )
    awal = fields.Float(string=u'Awal',digits=dp.get_precision('Custom 2'),)
    akhir = fields.Float(string=u'Akhir',digits=dp.get_precision('Custom 2'),)
    terpakai = fields.Float(string=u'Terpakai',digits=dp.get_precision('Custom 2'),)

    
    def get_hitung_qty_bom_line(self):
        self.qty_bom_reguler = 0.0
        self.qty_bom_soccer = 0.0
        #mengconvert dari gr ke kg
        self.qty_benang_kg = (self.qty_benang_gr/1000)
        #perhitungan toleransi
        toleransi_qty_bom_r = (self.qty_benang_kg*0.07)
        toleransi_qty_bom_s = (self.qty_benang_kg*0.15)
        #qty bom kaos kaki
        self.qty_bom_reguler = (self.qty_benang_kg + toleransi_qty_bom_r)
        self.qty_bom_soccer = (self.qty_benang_kg + toleransi_qty_bom_s)
        return

class MspAksesorisSampledevLine(models.Model):
    _name = 'msp.aksesoris.sampledev.line'

    msp_sample_dev_id = fields.Many2one('msp.sample.dev',string=u'msp sample dev',)
    #------------
    product_id = fields.Many2one('product.product',string=u'Nama Aksesoris',)
    jumlah_ambil = fields.Float(string=u'Jmlah Ambil',)


class OperatorMspSampleDevLine(models.Model):
    _name = 'operator.mspsample.dev.line'

    msp_sample_dev_id = fields.Many2one('msp.sample.dev',string=u'msp sample dev',)

    
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    nama_desain = fields.Char(string='Nama Desain',)
    berat = fields.Char(string='Berat',)
    waktu_produksi = fields.Char(string='Waktu Produksi',)
    tgl_buat = fields.Date(string='Tgl Buat',default=fields.Date.context_today,)
    nama_operator_id = fields.Many2one('hr.employee',string=u'Nama Operator',)


    gum_stretch_x= fields.Char(string='Gum Stretch x ',)
    gum_stretch_y= fields.Char(string='Gum Stretch y ',)
    leg_gum_stretch_x= fields.Char(string='Leg Gum Stretch x ',)
    leg_gum_stretch_y= fields.Char(string='Leg Gum Stretch y ',)
    leg_gum_atas_stretch_x= fields.Char(string='Leg Gum Atas Stretch x ',)
    leg_gum_atas_stretch_y= fields.Char(string='Leg Gum Atas Stretch y ',)
    leg_gum_bawah_stretch_x= fields.Char(string='Leg Gum Bawah Stretch x ',)
    leg_gum_bawah_stretch_y= fields.Char(string='Leg Gum Bawah Stretch y ',)
    leg_stretch_x= fields.Char(string=' Leg Stretch x',)
    leg_stretch_y= fields.Char(string='Leg Stretch y ',)
    foot_stretch_x= fields.Char(string=' Foot Stretch x',)
    foot_stretch_y= fields.Char(string=' Foot Stretch y',)
    foot_gum_stretch_x= fields.Char(string='Foot Gum Stretch x ',)
    foot_gum_stretch_y= fields.Char(string='Foot Gum Stretch y ',)
    hell_stretch_x= fields.Char(string='Heel Stretch x ',)
    hell_stretch_y= fields.Char(string='Heel Stretch y ',)

    gum_atas_stretch_x = fields.Char(string='Gum Atas Stretch X',)
    gum_atas_stretch_y = fields.Char(string='Gum Atas Stretch Y',)

    gum_bawah_stretch_x = fields.Char(string='Gum Bawah Stretch X',)
    gum_bawah_stretch_y = fields.Char(string='Gum Bawah Stretch Y' ,)


    leg_gum_atas_stretch_x = fields.Char(string='Leg Gum Atas Stretch X',)
    leg_gum_atas_stretch_y = fields.Char(string='Leg Gum Atas Stretch Y',)
    
    leg_gum_bawah_stretch_x = fields.Char(string='Leg Gum Bawah Stretch X',)
    leg_gum_bawah_stretch_y= fields.Char(string='Leg Gum Bawah Stretch Y',)
    
    leg_gum_tengah_stretch_x = fields.Char(string='Leg Gum Tengah Stretch X',)
    leg_gum_tengah_stretch_y = fields.Char(string='Leg Gum Tengah Stretch Y',)

    welt_inside_crc = fields.Char(string='Welt Inside CRC',)
    welt_inside_s = fields.Char(string='Welt Inside S',)
    welt_inside_e = fields.Char(string='Welt Inside E',)

    welt_outside_crc = fields.Char(string='Welt Outside CRC',)
    welt_outside_s = fields.Char(string='Welt Outside S',)
    welt_outside_e = fields.Char(string='Welt Outside E',)
    
    transfer_crc = fields.Char(string='Transfer CRC',)
    transfer_s = fields.Char(string='Transfer S',)
    transfer_e = fields.Char(string='Transfer E',)

    leg_gum_crc = fields.Char(string='Leg Gum CRC',)
    leg_gum_s = fields.Char(string='Leg Gum S',)
    leg_gum_e = fields.Char(string='Leg Gum E',)

    leg_crc = fields.Char(string='Leg CRC',)
    leg_s = fields.Char(string='Leg S',)
    leg_e = fields.Char(string='Leg E',)

    leg_band_elast_crc = fields.Char(string='Leg band Elast CRC',)
    leg_band_elast_s = fields.Char(string='Leg band Elast S',)
    leg_band_elast_e = fields.Char(string='Leg band Elast E',)

    ankle_crc = fields.Char(string='Ankle CRC',)
    ankle_s = fields.Char(string='Ankle S',)
    ankle_e = fields.Char(string='Ankle E',)

    heel_crc = fields.Char(string='Heel CRC',)
    heel_s = fields.Char(string='Heel S',)
    heel_e = fields.Char(string='Heel E',)

    foot_gum_crc = fields.Char(string='Foot Gum CRC',)
    foot_gum_s = fields.Char(string='Foot Gum S',)
    foot_gum_e = fields.Char(string='Foot Gum E',)

    foot_crc = fields.Char(string='Foot CRC',)
    foot_s = fields.Char(string='Foot S',)
    foot_e = fields.Char(string='Foot E',)

    begin_toe_crc = fields.Char(string='Begin Toe CRC',)
    begin_toe_s = fields.Char(string='Begin Toe S',)
    begin_toe_e = fields.Char(string='Begin Toe E',)

    toe_crc = fields.Char(string='Toe CRC',)
    toe_s = fields.Char(string='Toe S',)
    toe_e = fields.Char(string='Toe E',)

    rosso_crc = fields.Char(string='Rosso CRC',)
    rosso_s = fields.Char(string='Rosso S',)
    rosso_e = fields.Char(string='Rosso E',)

    lose_crc = fields.Char(string='Lose CRC',)
    lose_s = fields.Char(string='Lose S',)
    lose_e = fields.Char(string='Lose E',)

    lingking_crc = fields.Char(string='Lingking CRC',)
    lingking_s = fields.Char(string='Lingking S',)
    lingking_e = fields.Char(string='Lingking E',)

    
    feed_1 = fields.Char(string='Feed 1',)
    feed_1a = fields.Char(string='Feed 1A',)
    feed_1b = fields.Char(string='Feed 1B',)
    feed_1c = fields.Char(string='Feed 1C',)

    feed_2 = fields.Char(string='Feed 2',)
    feed_2a = fields.Char(string='Feed 2A',)
    feed_2b = fields.Char(string='Feed 2B',)
    feed_2c = fields.Char(string='Feed 2C',)

    feed_3_a = fields.Char(string='Feed 3.A',)
    feed_3a = fields.Char(string='Feed 3A',)
    feed_3_b = fields.Char(string='Feed 3.B',)
    feed_3b = fields.Char(string='Feed 3B',)
    feed_3c = fields.Char(string='Feed 3C',)

    feed_4_a = fields.Char(string='Feed 4.A',)
    feed_4a = fields.Char(string='Feed 4A',)
    feed_4_b = fields.Char(string='Feed 1',)
    feed_4b = fields.Char(string='Feed 4B',)

    feed_5 = fields.Char(string='Feed 5',)
    feed_5a = fields.Char(string='Feed 5A',)
    feed_5b = fields.Char(string='Feed 5B',)
    feed_5c = fields.Char(string='Feed 5C',)
    
    feed_6 = fields.Char(string='Feed 6',)
    feed_7 = fields.Char(string='Feed 7',)
    feed_8 = fields.Char(string='Feed 8',)

    tgl_buat_operator = fields.Date(string='Tgl Buat Operator',)
    feed_4c = fields.Char(string='Feed 4C',)

# --------------------------JENIS KAOS KAKI ---------------------------------------
class MarelInSamlpeJenisKk(models.Model):
    _name = 'marel.sample.jenis.kk'
    
    name = fields.Char(string='Name',)
    

class MarelInSamlpeBom(models.Model):
    _inherit = ['mrp.bom']

    janis_kk_id = fields.Many2one('marel.sample.jenis.kk',string='Janis Kk',store=True,)
    toleransi_antislip = fields.Float(string='Toleransi Antislip (%)',)
    
class MarelInSamlpeBomLine(models.Model):
    _inherit = ['mrp.bom.line']

    msp_sample_dev_id = fields.Many2one('msp.sample.dev',string=u'msp sample dev',)
    jumlah_ambil = fields.Float(string=u'Jmlah Ambil (C)',)
    qty_benang_kg = fields.Float(string=u'Qty Benang Per Pasang (kg)',digits=dp.get_precision('Custom 2'),)
    qty_benang_gr = fields.Float(string=u'Qty Benang Per Pasang (gr)',digits=dp.get_precision('Custom 2'),)
    qty_bom_reguler = fields.Float(string=u'Qty Bom (R)',digits=dp.get_precision('Custom 2'),)
    qty_bom_soccer = fields.Float(string=u'Qty Bom (S)',digits=dp.get_precision('Custom 2'),)
    awal = fields.Float(string=u'Awal',digits=dp.get_precision('Custom 2'),)
    akhir = fields.Float(string=u'Akhir',digits=dp.get_precision('Custom 2'),)
    terpakai = fields.Float(string=u'Terpakai',digits=dp.get_precision('Custom 2'),)


    
    def get_hitung_qty_mrp_bom_line(self):
        self.qty_bom_reguler = 0.0
        self.qty_bom_soccer = 0.0
        #mengconvert dari gr ke kg
        self.qty_benang_kg = (self.qty_benang_gr/1000)
        #perhitungan toleransi
        toleransi_qty_bom_r = (self.qty_benang_kg*0.07)
        toleransi_qty_bom_s = (self.qty_benang_kg*0.15)
        #qty bom kaos kaki
        self.qty_bom_reguler = (self.qty_benang_kg + toleransi_qty_bom_r)
        self.qty_bom_soccer = (self.qty_benang_kg + toleransi_qty_bom_s)

        if (self.bom_id.janis_kk_id.id == 1 and self.operation_id.workcenter_id.id != 5):
            self.product_qty = self.qty_bom_reguler
        elif (self.bom_id.janis_kk_id.id == 2 and self.operation_id.workcenter_id.id != 5):
            self.product_qty = self.qty_bom_soccer
        elif (self.operation_id.workcenter_id.id == 5):
            self.product_qty = (self.qty_benang_gr + (((self.bom_id.toleransi_antislip)/100)*self.qty_benang_gr))/1000



class MspSampleDev(models.Model):

    _name = 'msp.sample.dev'
    _rec_name = 'product_id'

    msp_sample_dev_line_ids = fields.One2many('msp.sample.dev.line','msp_sample_dev_id',string=u'Samlpe Dev Line',)
    operator_mspsample_dev_line_ids = fields.One2many('operator.mspsample.dev.line','msp_sample_dev_id',string=u'Oeprator Mengisi Sample',)
    msp_aksesoris_sampledev_line_ids = fields.One2many('msp.aksesoris.sampledev.line','msp_sample_dev_id',string=u'Aksesoris Samlpe Dev Line',)
    # mrp bom
    mrp_bom_line_ids = fields.One2many('mrp.bom.line','msp_sample_dev_id',string=u'BOM Line',related='product_id.bom_ids.bom_line_ids',)


    def _get_msp_sample_dev_no(self):
        nama_baru = self.env['ir.sequence'].next_by_code('msp.sample.dev.no')
        return nama_baru
    
    partner_id = fields.Many2one('res.users',string='Partner Id',)
    name = fields.Char(string='Id Sample',required=True,copy=False, default=_get_msp_sample_dev_no,readonly=True )
    tgl_masuk = fields.Date(string=u'Tgl Masuk',default=fields.Date.context_today,)
    tgl_selesai = fields.Datetime(string=u'Tgl Selesai',readonly=True)
    product_id = fields.Many2one('product.product',string=u'Nama Prodak',)
    kode_dokumen = fields.Char(string=u'Kode Doc',)
    gambar_sample = fields.Binary(string='Gambar Sample',)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    penjerat_2 = fields.Many2one('product.product',string=u'Penjerat 2',)

    size = fields.Float(string='Size',)
    waktu = fields.Float(string='Waktu Steam',)
    waktu_anti_slip = fields.Float(string='Waktu Anti Slip',)
    keterangan_anti_slip = fields.Text(string='keterangan AS',)

    no_mesin = fields.Float(string=u'No Mesin/Jarum',)
    warna = fields.Char(string=u'Warna',)
    keterangan = fields.Text(string='keterangan',)
    
    brand = fields.Char(string=u'Brand',)
    model_sample = fields.Char(string=u'Model',)
    tipe = fields.Char(string=u'Type',)
    delivery = fields.Datetime(string=u'Delivery',)

    gum_relaxed_x= fields.Float(string='Gum Relaxed x ',)
    gum_relaxed_y= fields.Float(string='Gum Relaxed y ',)

    leg_gum_relaxed_x= fields.Float(string='Leg Gum Relaxed x ',)
    leg_gum_relaxed_y= fields.Float(string='Leg Gum Relaxed y ',)

    leg_gum_atas_relaxed_x= fields.Float(string='Leg Gum Atas Relaxed x ',)
    leg_gum_atas_relaxed_y= fields.Float(string='Leg Gum Atas Relaxed y ',)

    leg_gum_bawah_relaxed_x= fields.Float(string='Leg Gum Bawah Relaxed x ',)
    leg_gum_bawah_relaxed_y= fields.Float(string='Leg Gum Bawah Relaxed y ',)

    leg_relaxed_x= fields.Float(string=' Leg Relaxed x',)
    leg_relaxed_y= fields.Float(string='Leg Relaxed y ',)

    foot_relaxed_x= fields.Float(string=' Foot Relaxed x',)
    foot_relaxed_y= fields.Float(string=' Foot Relaxed y',)

    foot_gum_relaxed_x= fields.Float(string='Foot Gum Relaxed x ',)
    foot_gum_relaxed_y= fields.Float(string='Foot Gum Relaxed y ',)

    hell_relaxed_x= fields.Float(string='Heel Relaxed x ',)
    hell_relaxed_y= fields.Float(string='Heel Relaxed y ',)

    gum_atas_relaxed_x = fields.Float(string='Gum Atas Relaxed X',)
    gum_atas_relaxed_y = fields.Float(string='Gum Atas Relaxed Y',)

    gum_bawah_relaxed_x = fields.Float(string='Gum Bawah relaxed X',)
    gum_bawah_relaxed_y = fields.Float(string='Gum Bawah Relaxed Y' ,)

    leg_gum_tengah_relaxed_x = fields.Float(string='Leg Gum Tengah Relaxed X',)
    leg_gum_tengah_relaxed_y = fields.Float(string='Leg Gum Tengah Relaxed Y',)
    
    gum_relaxed_out_x = fields.Float(string='Gum Relaxed Out X')
    gum_relaxed_out_y = fields.Float(string='Gum Relaxed Out Y')

    leg_gum_relaxed_out_x = fields.Float(string='Leg Gum Relaxed Out X')
    leg_gum_relaxed_out_y = fields.Float(string='Leg Gum Relaxed Out Y')

    leg_relaxed_out_x = fields.Float(string='Leg Relaxed Out X')
    leg_relaxed_out_y = fields.Float(string='Leg Relaxed Out Y')

    foot_relaxed_out_x = fields.Float(string='Foot Relaxed Out X')
    foot_relaxed_out_y = fields.Float(string='Foot Relaxed Out Y')

    foot_gum_relaxed_out_x = fields.Float(string='Foot Gum Relaxed Out X')
    foot_gum_relaxed_out_y = fields.Float(string='Foot Gum Relaxed Out Y')

    heel_relaxed_out_x = fields.Float(string='Heel Relaxed Out X')
    heel_relaxed_out_y = fields.Float(string='Heel Relaxed Out Y')

    leg_gum_atas_relaxed_out_x = fields.Float(string='Leg Gum Atas Relaxed Out X')
    leg_gum_atas_relaxed_out_y = fields.Float(string='Leg Gum Atas Relaxed Out Y')
 
    leg_gum_bawah_relaxed_out_x = fields.Float(string='Leg Gum Bawah Relaxed Out X')
    leg_gum_bawah_relaxed_out_y = fields.Float(string='Leg Gum Bawah Relaxed Out Y')

    leg_gum_tengah_relaxed_out_x = fields.Float(string='Leg Gum Tengah Relaxed Out X')
    leg_gum_tengah_relaxed_out_y = fields.Float(string='Leg Gum Tengah Relaxed Out Y')

    gum_atas_relaxed_out_x = fields.Float(string='Gum Atas Relaxed Out X')
    gum_atas_relaxed_out_y = fields.Float(string='Gum Atas Relaxed Out Y')

    gum_bawah_relaxed_out_x = fields.Float(string='Gum Bawah Relaxed Out X')
    gum_bawah_relaxed_out_y = fields.Float(string='Gum Bawah Relaxed Out Y ')
    
    
    style = fields.Char(string=u'Style',)
    artikel = fields.Char(string=u'Artikel',)
    body = fields.Many2one('product.product',string=u'Body',)
    wording_munich = fields.Many2one('product.product',string=u'Wording',)
    logo = fields.Many2one('product.product',string=u'Logo',)
    hell = fields.Many2one('product.product',string=u'Heel',)
    toe = fields.Many2one('product.product',string=u'Toe',)
    transfer = fields.Many2one('product.product',string=u'Transfer',)
    lintoe = fields.Many2one('product.product',string=u'Lintoe',)
    penjerat = fields.Many2one('product.product',string=u'Penjerat',)
    karet = fields.Many2one('product.product',string=u'Karet',)
    patter_1 = fields.Many2one('product.product',string=u'Pattern 1',)
    patter_2 = fields.Many2one('product.product',string=u'Pattern 2',)
    patter_3 = fields.Many2one('product.product',string=u'Pattern 3',)
    patter_4 = fields.Many2one('product.product',string=u'Pattern 4',)
    patter_5 = fields.Many2one('product.product',string=u'Pattern 5',)
    patter_6 = fields.Many2one('product.product',string=u'Pattern 6',)
    patter_7 = fields.Many2one('product.product',string=u'Pattern 7',)
    patter_8 = fields.Many2one('product.product',string=u'Pattern 8',)
    patter_9 = fields.Many2one('product.product',string=u'Pattern 9',)
    patter_10 = fields.Many2one('product.product',string=u'Pattern 10',)
    jumlah_pasang = fields.Integer(string='Jumlah Pasang',)

    #untuk BOM Benang
    needle = fields.Char(string=u'Needle',)
    nama_sample = fields.Char(string=u'Nama Sample',)
    tgl_bon = fields.Date(string=u'Tgl Permintaan BON',default=fields.Date.context_today,)

    partner_id = fields.Many2one('res.partner', string='Customer',)
    state = fields.Selection([
        ('draft', 'Open'),
        ('done','Done'),
        ('cancel','Canceled')
        ],string="Status", readonly=True, copy=False, default='draft')
                            
    
    def action_close(self):
        tgl_selesai = fields.Datetime.now()
        self.write({'state': 'done','tgl_selesai':tgl_selesai})
    
    def action_set_draft(self):
        self.write({'state': 'draft'})

    # TOTAL BRUTO
    total_bruto = fields.Float(string='Total Bruto',compute='_get_jumlah_total_bruto',store=True)


    def _get_copy_data_sample (self):
        for l in self:
            if l.product_id :
                l.product_id.product_tmpl_id.kode_dokumen = l.kode_dokumen
                l.product_id.product_tmpl_id.gambar_sample = l.gambar_sample
                l.product_id.product_tmpl_id.penjerat_2 = l.penjerat_2
                l.product_id.product_tmpl_id.size = l.size
                l.product_id.product_tmpl_id.waktu = l.waktu
                l.product_id.product_tmpl_id.waktu_anti_slip = l.waktu_anti_slip
                l.product_id.product_tmpl_id.keterangan_anti_slip = l.keterangan_anti_slip
                l.product_id.product_tmpl_id.no_mesin = l.no_mesin
                l.product_id.product_tmpl_id.warna = l.warna
                l.product_id.product_tmpl_id.keterangan = l.keterangan
                l.product_id.product_tmpl_id.brand = l.brand
                l.product_id.product_tmpl_id.model_sample = l.model_sample
                l.product_id.product_tmpl_id.tipe = l.tipe
                l.product_id.product_tmpl_id.gum_relaxed_x = l.gum_relaxed_x
                l.product_id.product_tmpl_id.gum_relaxed_y = l.gum_relaxed_y
                l.product_id.product_tmpl_id.leg_gum_relaxed_x = l.leg_gum_relaxed_x
                l.product_id.product_tmpl_id.leg_gum_relaxed_y = l.leg_gum_relaxed_y
                l.product_id.product_tmpl_id.leg_gum_atas_relaxed_x = l.leg_gum_atas_relaxed_x
                l.product_id.product_tmpl_id.leg_gum_atas_relaxed_y = l.leg_gum_atas_relaxed_y
                l.product_id.product_tmpl_id.leg_gum_bawah_relaxed_x = l.leg_gum_bawah_relaxed_x
                l.product_id.product_tmpl_id.leg_gum_bawah_relaxed_y = l.leg_gum_bawah_relaxed_y
                l.product_id.product_tmpl_id.leg_relaxed_x = l.leg_relaxed_x
                l.product_id.product_tmpl_id.leg_relaxed_y = l.leg_relaxed_y
                l.product_id.product_tmpl_id.foot_relaxed_x = l.foot_relaxed_x
                l.product_id.product_tmpl_id.foot_relaxed_y = l.foot_relaxed_y
                l.product_id.product_tmpl_id.foot_gum_relaxed_x = l.foot_gum_relaxed_x
                l.product_id.product_tmpl_id.foot_gum_relaxed_y = l.foot_gum_relaxed_y
                l.product_id.product_tmpl_id.hell_relaxed_x = l.hell_relaxed_x
                l.product_id.product_tmpl_id.hell_relaxed_y = l.hell_relaxed_y
                l.product_id.product_tmpl_id.gum_atas_relaxed_x = l.gum_atas_relaxed_x
                l.product_id.product_tmpl_id.gum_atas_relaxed_y = l.gum_atas_relaxed_y
                l.product_id.product_tmpl_id.gum_bawah_relaxed_x = l.gum_bawah_relaxed_x
                l.product_id.product_tmpl_id.gum_bawah_relaxed_y = l.gum_bawah_relaxed_y
                l.product_id.product_tmpl_id.leg_gum_tengah_relaxed_x = l.leg_gum_tengah_relaxed_x
                l.product_id.product_tmpl_id.leg_gum_tengah_relaxed_y = l.leg_gum_tengah_relaxed_y
                l.product_id.product_tmpl_id.style = l.style
                l.product_id.product_tmpl_id.artikel = l.artikel
                l.product_id.product_tmpl_id.body = l.body
                l.product_id.product_tmpl_id.wording_munich = l.wording_munich
                l.product_id.product_tmpl_id.logo = l.logo
                l.product_id.product_tmpl_id.hell = l.hell
                l.product_id.product_tmpl_id.toe = l.toe
                l.product_id.product_tmpl_id.transfer = l.transfer
                l.product_id.product_tmpl_id.lintoe = l.lintoe
                l.product_id.product_tmpl_id.penjerat = l.penjerat
                l.product_id.product_tmpl_id.karet = l.karet
                l.product_id.product_tmpl_id.patter_1 = l.patter_1
                l.product_id.product_tmpl_id.patter_2 = l.patter_2
                l.product_id.product_tmpl_id.patter_3 = l.patter_3
                l.product_id.product_tmpl_id.patter_4 = l.patter_4
                l.product_id.product_tmpl_id.patter_5 = l.patter_5
                l.product_id.product_tmpl_id.patter_6 = l.patter_6
                l.product_id.product_tmpl_id.patter_7 = l.patter_7
                l.product_id.product_tmpl_id.patter_8 = l.patter_8
                l.product_id.product_tmpl_id.patter_9 = l.patter_9
                l.product_id.product_tmpl_id.patter_10 = l.patter_10
                l.product_id.product_tmpl_id.needle = l.needle
                l.product_id.product_tmpl_id.nama_sample = l.nama_sample

    @api.depends('mrp_bom_line_ids')
    def _get_jumlah_total_bruto(self):
        for msp_sample_dev_id in self:
            msp_sample_dev_id.total_bruto = sum((line_id.terpakai) for line_id in msp_sample_dev_id.mrp_bom_line_ids)
            msp_sample_dev_id._get_copy_data_sample()


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    kode_dokumen = fields.Char(string=u'Kode Doc',)
    gambar_sample = fields.Binary(string='Gambar Sample',)

    penjerat_2 = fields.Many2one('product.product',string=u'Penjerat 2',)

    size = fields.Float(string='Size',)
    waktu = fields.Float(string='Waktu Steam',)
    waktu_anti_slip = fields.Float(string='Waktu Anti Slip',)
    keterangan_anti_slip = fields.Text(string='keterangan AS',)

    no_mesin = fields.Float(string=u'No Mesin/Jarum',)
    warna = fields.Char(string=u'Warna',)
    keterangan = fields.Text(string='keterangan',)
    
    brand = fields.Char(string=u'Brand',)
    model_sample = fields.Char(string=u'Model',)
    tipe = fields.Char(string=u'Type',)

    gum_relaxed_x= fields.Float(string='Gum Relaxed x ',)
    gum_relaxed_y= fields.Float(string='Gum Relaxed y ',)

    leg_gum_relaxed_x= fields.Float(string='Leg Gum Relaxed x ',)
    leg_gum_relaxed_y= fields.Float(string='Leg Gum Relaxed y ',)

    leg_gum_atas_relaxed_x= fields.Float(string='Leg Gum Atas Relaxed x ',)
    leg_gum_atas_relaxed_y= fields.Float(string='Leg Gum Atas Relaxed y ',)

    leg_gum_bawah_relaxed_x= fields.Float(string='Leg Gum Bawah Relaxed x ',)
    leg_gum_bawah_relaxed_y= fields.Float(string='Leg Gum Bawah Relaxed y ',)

    leg_relaxed_x= fields.Float(string=' Leg Relaxed x',)
    leg_relaxed_y= fields.Float(string='Leg Relaxed y ',)

    foot_relaxed_x= fields.Float(string=' Foot Relaxed x',)
    foot_relaxed_y= fields.Float(string=' Foot Relaxed y',)

    foot_gum_relaxed_x= fields.Float(string='Foot Gum Relaxed x ',)
    foot_gum_relaxed_y= fields.Float(string='Foot Gum Relaxed y ',)

    hell_relaxed_x= fields.Float(string='Heel Relaxed x ',)
    hell_relaxed_y= fields.Float(string='Heel Relaxed y ',)

    gum_atas_relaxed_x = fields.Float(string='Gum Atas Relaxed X',)
    gum_atas_relaxed_y = fields.Float(string='Gum Atas Relaxed Y',)

    gum_bawah_relaxed_x = fields.Float(string='Gum Bawah relaxed X',)
    gum_bawah_relaxed_y = fields.Float(string='Gum Bawah Relaxed Y' ,)

    leg_gum_tengah_relaxed_x = fields.Float(string='Leg Gum Tengah Relaxed X',)
    leg_gum_tengah_relaxed_y = fields.Float(string='Leg Gum Tengah Relaxed Y',)
    
    
    style = fields.Char(string=u'Style',)
    artikel = fields.Char(string=u'Artikel',)
    body = fields.Many2one('product.product',string=u'Body',)
    wording_munich = fields.Many2one('product.product',string=u'Wording',)
    logo = fields.Many2one('product.product',string=u'Logo',)
    hell = fields.Many2one('product.product',string=u'Heel',)
    toe = fields.Many2one('product.product',string=u'Toe',)
    transfer = fields.Many2one('product.product',string=u'Transfer',)
    lintoe = fields.Many2one('product.product',string=u'Lintoe',)
    penjerat = fields.Many2one('product.product',string=u'Penjerat',)
    karet = fields.Many2one('product.product',string=u'Karet',)
    patter_1 = fields.Many2one('product.product',string=u'Pattern 1',)
    patter_2 = fields.Many2one('product.product',string=u'Pattern 2',)
    patter_3 = fields.Many2one('product.product',string=u'Pattern 3',)
    patter_4 = fields.Many2one('product.product',string=u'Pattern 4',)
    patter_5 = fields.Many2one('product.product',string=u'Pattern 5',)
    patter_6 = fields.Many2one('product.product',string=u'Pattern 6',)
    patter_7 = fields.Many2one('product.product',string=u'Pattern 7',)
    patter_8 = fields.Many2one('product.product',string=u'Pattern 8',)
    patter_9 = fields.Many2one('product.product',string=u'Pattern 9',)
    patter_10 = fields.Many2one('product.product',string=u'Pattern 10',)
    jumlah_pasang = fields.Integer(string='Jumlah Pasang',)

    #untuk BOM Benang
    needle = fields.Char(string=u'Needle',)
    nama_sample = fields.Char(string=u'Nama Sample',)

    