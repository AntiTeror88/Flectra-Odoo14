from odoo.addons import decimal_precision as dp
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.tools import float_round

class MspSetNote(models.Model):
    _name = 'msp.set.note'
    
    name = fields.Char(string='name',store=True,)
    note_lokal = fields.Text(string='Note Lokal',store=True,)
    note_import = fields.Text(string='Note Import',store=True,)

class MarelInPurchase(models.Model):
    _inherit = ['purchase.order']
    
    msp_set_note_id = fields.Many2one('msp.set.note',string='Msp Set Note',store=True,)
    note_lokal = fields.Text(string='Note Lokal',compute="_compute_note_lokal",store=True,)
    note_import = fields.Text(string='Note Import',compute="_compute_note_import",store=True,)


    @api.depends("msp_set_note_id")
    def _compute_note_lokal(self):
        for l in self:
            if l.po_local :
                l.note_lokal = l.msp_set_note_id.note_lokal

    @api.depends("msp_set_note_id")
    def _compute_note_import(self):
        for l in self:
            if l.po_import :
                l.note_import = l.msp_set_note_id.note_import