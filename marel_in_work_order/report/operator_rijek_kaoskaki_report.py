# -*- coding: utf-8 -*-
# Part of Odoo, odoo. See LICENSE file for full copyright and licensing details.

#
# Please note that these reports are not multi-currency !!!
#

from odoo import api, fields, models, tools


class OperatorRijekKaoskakiReport(models.Model):
    _name = "operator.rijek.kaoskaki.report"
    _description = "Operator Rijek Kaoskaki Report"
    _auto = False
    # _order = 'date_order desc, price_total desc'


# table jenis.rijek.kaoskaki
    nama_rijek = fields.Char(string='Jenis Rijek',readonly=True)

# table operator.rijek.kaoskaki
    # jenis_rijek_kaoskaki_id = fields.Many2one('jenis.rijek.kaoskaki',string='Jenis Rijek Kaoskaki',readonly=True)
    keterangan = fields.Text(string='keterangan',readonly=True)
    jumlah_rjk = fields.Integer( string='Jumlah Rijek',readonly=True)
    marel_nama_operatorlist_id = fields.Many2one('marel.nama.operatorlist',string='Nama Operatorlist',readonly=True)
    
# table marel.nama.operatorlist
    nama_operator_work_order_id = fields.Many2one('mrp.workorder', 'Routing', readonly=True)
    workcenter_id = fields.Many2one('mrp.workcenter', 'Work Center', related='nama_operator_work_order_id.workcenter_id',)
    shift = fields.Selection([
        ('A','A'),
        ('B','B'),
	    ('C','C'),], string="Shift",readonly=True)

    no_kkp = fields.Char(string=u'No KKP',readonly=True)
    # jumlah_reject = fields.Integer(string=u'Jumlah Reject',readonly=True)
    tgl_kerja = fields.Date(string=u'tgl Kerja',default=fields.Date.context_today,readonly=True)
    jumlah_yg_selesai = fields.Integer(string=u'Qty Yg Selesai',readonly=True)
    krono_kk_menit = fields.Float(string=u'Krono KK (menit)',readonly=True)
    target_kk_operator = fields.Integer(string=u'Target Knitting',readonly=True)
    nama_operator_id = fields.Many2one('marel.nama.operator',string=u'Nama Operator',)
    nama_qiusi_id = fields.Many2one('marel.nama.qiusi',string=u'Nama qiusi',)
    no_mesin_id = fields.Many2one('mesin.marel.produksi',string=u'No Mesin',)
 
# table mrp.workorder
    production_id = fields.Many2one('mrp.production',string='No MO',readonly=True)
    # no_so = fields.Char(related='production_id.origin',string=u'No So',readonly=True)
    target_conti = fields.Integer(string='Target Conti',readonly=True)
    target_as = fields.Integer(string='Target Anti Slip',readonly=True)
    target_sewing = fields.Integer(string='Target Sewing',readonly=True)
    target_bordir = fields.Integer(string='Target Bordir',readonly=True)
    target_setting = fields.Integer(string='Target Setting',readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', related='product_id.product_tmpl_id', readonly=True)


# query report
    @api.model_cr
    def init(self):
        """ Marel Perbaikan Kerusakan Mesin """
        tools.drop_view_if_exists(self._cr, 'operator_rijek_kaoskaki_report')
        self._cr.execute(""" CREATE VIEW operator_rijek_kaoskaki_report AS (
            SELECT
                mnol.id as id,
                ork.keterangan as keterangan,
                ork.jumlah_rjk as jumlah_rjk,
                ork.marel_nama_operatorlist_id as marel_nama_operatorlist_id,
                jrk.name as nama_rijek,
                mnol.shift as shift,
                mnol.no_kkp as no_kkp,
                mnol.tgl_kerja as tgl_kerja,
                mnol.jumlah_yg_selesai as jumlah_yg_selesai,
                mnol.krono_kk_menit as krono_kk_menit,
                mnol.target_kk_operator as target_kk_operator,
                mnol.nama_operator_id as nama_operator_id,
                mnol.nama_qiusi_id as nama_qiusi_id,
                mwo.workcenter_id as workcenter_id,
                mnol.no_mesin_id as no_mesin_id,
                mnol.nama_operator_work_order_id as nama_operator_work_order_id,
                mnol.target_conti as target_conti,
                mnol.target_as as target_as,
                mnol.target_sewing as target_sewing,
                mnol.target_bordir as target_bordir,
                mnol.target_setting as target_setting,
                mwo.product_id as product_id,
                mwo.production_id as production_id
            FROM
                marel_nama_operatorlist mnol
            LEFT JOIN
                operator_rijek_kaoskaki ork ON (ork.marel_nama_operatorlist_id = mnol.id)
            LEFT JOIN
                jenis_rijek_kaoskaki jrk ON (ork.jenis_rijek_kaoskaki_id = jrk.id)
            LEFT JOIN
                mrp_workorder mwo ON (mnol.nama_operator_work_order_id = mwo.id)
            JOIN
                product_product pp ON (mwo.product_id = pp.id)
            JOIN 
                product_template pt ON (pp.product_tmpl_id = pt.id)
            GROUP BY
                mnol.id,
                ork.keterangan,
                ork.jumlah_rjk,
                ork.marel_nama_operatorlist_id ,
                jrk.name,
                mnol.shift,
                mnol.no_kkp ,
                mnol.tgl_kerja,
                mnol.jumlah_yg_selesai,
                mnol.krono_kk_menit,
                mnol.target_kk_operator,
                mnol.nama_operator_id ,
                mnol.nama_qiusi_id ,
                mwo.workcenter_id ,
                mnol.no_mesin_id,
                mnol.nama_operator_work_order_id,
                mnol.target_conti ,
                mnol.target_as,
                mnol.target_sewing ,
                mnol.target_bordir,
                mnol.target_setting,
                mwo.product_id,
                mwo.production_id
        )""")
