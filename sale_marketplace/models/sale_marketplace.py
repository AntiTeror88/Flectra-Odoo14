from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_order = fields.Datetime(string='Order Date', required=True, readonly=False, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    sale_marketplace = fields.Many2one ('market.place', 'Marketplace')

    _sql_constraints = [
        ('customer_reference_unique_type', 'UNIQUE(client_order_ref)', 'This reference has been used.'),
    ]

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.sale_marketplace:
            invoice_vals.update({
                'invoice_marketplace': self.sale_marketplace.id,
            })
        return invoice_vals

class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_marketplace = fields.Many2one ('market.place', 'Marketplace')


class SaleOrderLine(models.Model):
    _inherit = "account.move.line"

    invoice_marketplace = fields.Many2one ('market.place', string='Marketplace', related='move_id.invoice_marketplace', store=True)

class SaleLine(models.Model):
    _inherit = "sale.order.line"

    analytic_account_id = fields.Many2one ('account.analytic.account', string='Analytic', related='order_id.analytic_account_id', store=True)