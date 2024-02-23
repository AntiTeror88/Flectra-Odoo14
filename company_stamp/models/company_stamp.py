# Copyright 2014 Therp BV (<http://therp.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class CompanyStamp(models.Model):
    _inherit = 'res.company'

    stamp = fields.Binary(string="Company Stamp")

class InvoiceStamp(models.Model):
    _inherit = 'account.move'

    is_stamp = fields.Boolean(string="Company Stamp")

class PurchaseStamp(models.Model):
    _inherit = 'purchase.order'

    is_stamp = fields.Boolean(string="Company Stamp")

class SaleStamp(models.Model):
    _inherit = 'sale.order'

    is_stamp = fields.Boolean(string="Company Stamp")
