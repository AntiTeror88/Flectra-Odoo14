from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SOPrintingStatus(models.Model):
    _inherit = 'sale.order'

    printed_so = fields.Selection([
        ('notprinted', 'Not Printed'),
        ('printed', 'Printed'),
        ], string='Print Status', store=True, readonly=True, default='notprinted')

    def print_sale(self):
        self.write({'printed_so': "printed"})
        return self.env.ref('sale.action_report_saleorder').report_action(self)


class POPrintingStatus(models.Model):
    _inherit = 'purchase.order'

    printed_po = fields.Selection([
        ('notprinted', 'Not Printed'),
        ('printed', 'Printed'),
        ], string='Print Status', store=True, readonly=True, default='notprinted')

    def print_purchase(self):
        self.write({'printed_po': "printed"})
        return self.env.ref('purchase.action_report_purchase_order').report_action(self)


class InvPrintingStatus(models.Model):
    _inherit = 'account.move'

    printed_invoice = fields.Selection([
        ('notprinted', 'Not Printed'),
        ('printed', 'Printed'),
        ], string='Print Status', store=True, readonly=True, default='notprinted')

    def print_invoice(self):
        if self.printed_invoice != 'printed':
            self.write({'printed_invoice': "printed"})
        return self.env.ref('account.account_invoices').report_action(self)

    def action_invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        if any(not move.is_invoice(include_receipts=True) for move in self):
            raise UserError(_("Only invoices could be printed."))

        self.filtered(lambda inv: not inv.invoice_sent).write({
            'invoice_sent': True,
            'printed_invoice': 'printed'
            })
        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref('account.account_invoices').report_action(self)
        else:
            return self.env.ref('account.account_invoices_without_payment').report_action(self)