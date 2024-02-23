# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api

from functools import lru_cache


class InvoicePerform(models.Model):
    _name = "invoice.perform"
    _description = "Invoices Perform"
    _auto = False
    _rec_name = 'invoice_date'
    _order = 'invoice_date desc'

    # ==== Invoice fields ====
    move_id = fields.Many2one('account.move', readonly=True)
    name = fields.Char('Invoice #', readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', string='Partner Company', help="Commercial Entity")
    country_id = fields.Many2one('res.country', string="Country")
    invoice_user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    move_type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Vendor Bill'),
        ('out_refund', 'Customer Credit Note'),
        ('in_refund', 'Vendor Credit Note'),
        ], readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Open'),
        ('cancel', 'Cancelled')
        ], string='Invoice Status', readonly=True)
    payment_state = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'paid')
    ], string='Payment Status', readonly=True)
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position', readonly=True)
    invoice_date = fields.Date(readonly=True, string="Invoice Date")
    invoice_payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', readonly=True)
    partner_bank_id = fields.Many2one('res.partner.bank', string='Bank Account', readonly=True)
    nbr_lines = fields.Integer(string='Line Count', readonly=True)
    residual = fields.Float(string='Due Amount', readonly=True)
    amount_total = fields.Float(string='Total', readonly=True)

    # ==== Invoice line fields ====
    quantity = fields.Float(string='Product Quantity', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', readonly=True)
    product_categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    invoice_date_due = fields.Date(string='Due Date', readonly=True)
    account_id = fields.Many2one('account.account', string='Revenue/Expense Account', readonly=True, domain=[('deprecated', '=', False)])
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', groups="analytic.group_analytic_accounting")
    price_subtotal = fields.Float(string='Untaxed Total', readonly=True)
    price_average = fields.Float(string='Average Price', readonly=True, group_operator="avg")

    _depends = {
        'account.move': [
            'name', 'state', 'move_type', 'partner_id', 'invoice_user_id', 'fiscal_position_id',
            'invoice_date', 'invoice_date_due', 'invoice_payment_term_id', 'partner_bank_id',
        ],
        'account.move.line': [
            'quantity', 'price_subtotal', 'amount_residual', 'balance', 'amount_currency',
            'move_id', 'product_id', 'product_uom_id', 'account_id', 'analytic_account_id',
            'journal_id', 'company_id', 'currency_id', 'partner_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    @api.model
    def _select(self):
        return '''
            SELECT
                line.id,
                line.move_id,
                line.product_id,
                line.account_id,
                line.analytic_account_id,
                line.journal_id,
                line.company_id,
                line.company_currency_id                                    AS currency_id,
                line.partner_id AS commercial_partner_id,
                move.name,
                move.state,
                move.move_type,
                move.partner_id,
                move.invoice_user_id,
                move.fiscal_position_id,
                move.payment_state,
                move.invoice_date,
                move.invoice_date_due,
                move.invoice_payment_term_id,
                move.partner_bank_id,
                -line.balance * (move.amount_residual_signed / NULLIF(move.amount_total_signed, 0.0)) * (line.price_total / NULLIF(line.price_subtotal, 0.0))
                                                                            AS residual,
                -line.balance * (line.price_total / NULLIF(line.price_subtotal, 0.0))    AS amount_total,
                uom_template.id                                             AS product_uom_id,
                template.categ_id                                           AS product_categ_id,
                line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0)
                                                                            AS quantity,
                -line.balance                                               AS price_subtotal,
                -line.balance / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0)
                                                                            AS price_average,
                COALESCE(partner.country_id, commercial_partner.country_id) AS country_id,
                1                                                           AS nbr_lines
        '''

    @api.model
    def _from(self):
        return '''
            FROM account_move_line line
                LEFT JOIN res_partner partner ON partner.id = line.partner_id
                LEFT JOIN product_product product ON product.id = line.product_id
                LEFT JOIN account_account account ON account.id = line.account_id
                LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                INNER JOIN account_move move ON move.id = line.move_id
                LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id
        '''

    @api.model
    def _where(self):
        return '''
            WHERE move.type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                AND line.account_id IS NOT NULL
                AND NOT line.exclude_from_invoice_tab
        '''

    @api.model
    def _group_by(self):
        return '''
            GROUP BY
                line.id,
                line.move_id,
                line.product_id,
                line.account_id,
                line.analytic_account_id,
                line.journal_id,
                line.company_id,
                line.currency_id,
                line.partner_id,
                move.name,
                move.state,
                move.move_type,
                move.amount_residual_signed,
                move.amount_total_signed,
                move.partner_id,
                move.invoice_user_id,
                move.fiscal_position_id,
                move.payment_state,
                move.invoice_date,
                move.invoice_date_due,
                move.invoice_payment_term_id,
                move.partner_bank_id,
                uom_template.id,
                uom_line.factor,
                template.categ_id,
                COALESCE(partner.country_id, commercial_partner.country_id)
        '''

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
                %s %s %s %s
            )
        ''' % (
            self._table, self._select(), self._from(), self._where(), self._group_by()
        ))

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        @lru_cache(maxsize=32)  # cache to prevent a SQL query for each data point
        def get_rate(currency_id):
            return self.env['res.currency']._get_conversion_rate(
                self.env['res.currency'].browse(currency_id),
                self.env.company.currency_id,
                self.env.company,
                self._fields['invoice_date'].today()
            )

        # First we get the structure of the results. The results won't be correct in multi-currency,
        # but we need this result structure.
        # By adding 'ids:array_agg(id)' to the fields, we will be able to map the results of the
        # second step in the structure of the first step.
        result_ref = super(AccountInvoiceReport, self).read_group(
            domain, fields + ['ids:array_agg(id)'], groupby, offset, limit, orderby, lazy
        )

        # In mono-currency, the results are correct, so we don't need the second step.
        if len(self.env.companies.mapped('currency_id')) <= 1:
            return result_ref

        # Reset all fields needing recomputation.
        for res_ref in result_ref:
            for field in {'amount_total', 'price_average', 'price_subtotal', 'residual'} & set(res_ref):
                res_ref[field] = 0.0

        # Then we perform another read_group, but this time we group by 'currency_id'. This way, we
        # are able to convert in batch in the current company currency.
        # During the process, we fill in the result structure we got in the previous step. To make
        # the mapping, we use the aggregated ids.
        result = super(AccountInvoiceReport, self).read_group(
            domain, fields + ['ids:array_agg(id)'], set(groupby) | {'currency_id'}, offset, limit, orderby, lazy
        )
        for res in result:
            if res.get('currency_id') and self.env.company.currency_id.id != res['currency_id'][0]:
                for field in {'amount_total', 'price_average', 'price_subtotal', 'residual'} & set(res):
                    res[field] = self.env.company.currency_id.round((res[field] or 0.0) * get_rate(res['currency_id'][0]))
            # Since the size of result_ref should be resonable, it should be fine to loop inside a
            # loop.
            for res_ref in result_ref:
                if res.get('ids') and res_ref.get('ids') and set(res['ids']) <= set(res_ref['ids']):
                    for field in {'amount_total', 'price_subtotal', 'residual'} & set(res_ref):
                        res_ref[field] += res[field]
                    for field in {'price_average'} & set(res_ref):
                        res_ref[field] = (res_ref[field] + res[field]) / 2 if res_ref[field] else res[field]

        return result_ref



# # -*- coding: utf-8 -*-

# from odoo import tools
# from odoo import models, fields, api


# class InvoicePerform (models.Model):
#     _name = "invoice.perform"
#     _inherit = ['ir.branch.company.mixin']
#     _description = "Invoices Performs"
#     _auto = False
#     _rec_name = 'date'

#     @api.multi
#     @api.depends('currency_id', 'date', 'price_total', 'price_average', 'residual')
#     def _compute_amounts_in_user_currency(self):
#         """Compute the amounts in the currency of the user
#         """
#         context = dict(self._context or {})
#         user_currency_id = self.env.user.company_id.currency_id
#         currency_rate_id = self.env['res.currency.rate'].search([
#             ('rate', '=', 1),
#             '|', ('company_id', '=', self.env.user.company_id.id), ('company_id', '=', False)], limit=1)
#         base_currency_id = currency_rate_id.currency_id
#         ctx = context.copy()
#         for record in self:
#             ctx['date'] = record.date
#             record.user_currency_price_total = base_currency_id.with_context(ctx).compute(record.price_total, user_currency_id)
#             record.user_currency_price_average = base_currency_id.with_context(ctx).compute(record.price_average, user_currency_id)
#             record.user_currency_residual = base_currency_id.with_context(ctx).compute(record.residual, user_currency_id)

#     date = fields.Date(readonly=True)
#     product_id = fields.Many2one('product.product', string='Product', readonly=True)
#     product_name = fields.Char(string='Name', readonly=True)
#     product_qty = fields.Float(string='Product Quantity', readonly=True)
#     uom_name = fields.Char(string='Reference Unit of Measure', readonly=True)
#     payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term', readonly=True)
#     fiscal_position_id = fields.Many2one('account.fiscal.position', oldname='fiscal_position', string='Fiscal Position', readonly=True)
#     currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
#     categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
#     journal_id = fields.Many2one('account.journal', string='Journal', readonly=True)
#     partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
#     commercial_partner_id = fields.Many2one('res.partner', string='Partner Company', help="Commercial Entity")
#     company_id = fields.Many2one('res.company', string='Company', readonly=True)
#     user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
#     price_total = fields.Float(string='Total Without Tax', readonly=True)
#     user_currency_price_total = fields.Float(string="Total Without Tax", compute='_compute_amounts_in_user_currency', digits=0)
#     price_average = fields.Float(string='Average Price', readonly=True, group_operator="avg")
#     user_currency_price_average = fields.Float(string="Average Price", compute='_compute_amounts_in_user_currency', digits=0)
#     currency_rate = fields.Float(string='Currency Rate', readonly=True, group_operator="avg", groups="base.group_multi_currency")
#     nbr = fields.Integer(string='# of Lines', readonly=True)  # TDE FIXME master: rename into nbr_lines
#     type = fields.Selection([
#         ('out_invoice', 'Customer Invoice'),
#         ('in_invoice', 'Vendor Bill'),
#         ('out_refund', 'Customer Credit Note'),
#         ('in_refund', 'Vendor Credit Note'),
#         ], readonly=True)
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('open', 'Open'),
#         ('paid', 'Paid'),
#         ('cancel', 'Cancelled')
#         ], string='Invoice Status', readonly=True)
#     date_due = fields.Date(string='Due Date', readonly=True)
#     account_id = fields.Many2one('account.account', string='Account', readonly=True, domain=[('deprecated', '=', False)])
#     account_line_id = fields.Many2one('account.account', string='Account Line', readonly=True, domain=[('deprecated', '=', False)])
#     partner_bank_id = fields.Many2one('res.partner.bank', string='Bank Account', readonly=True)
#     residual = fields.Float(string='Due Amount', readonly=True)
#     user_currency_residual = fields.Float(string="Total Residual", compute='_compute_amounts_in_user_currency', digits=0)
#     country_id = fields.Many2one('res.country', string='Country of the Partner Company')
#     account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account', groups="analytic.group_analytic_accounting")

#     _order = 'date desc'

#     _depends = {
#         'account.move': [
#             'account_id', 'amount_total_company_signed', 'commercial_partner_id', 'company_id', 'branch_id',
#             'currency_id', 'date_due', 'date_invoice', 'fiscal_position_id',
#             'journal_id', 'partner_bank_id', 'partner_id', 'payment_term_id',
#             'residual', 'state', 'type', 'user_id',
#         ],
#         'account.move.line': [
#             'account_id', 'invoice_id', 'price_subtotal', 'product_id',
#             'quantity', 'uom_id', 'account_analytic_id',
#         ],
#         'product.product': ['product_tmpl_id'],
#         'product.template': ['categ_id', 'name'],
#         'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
#         'res.currency.rate': ['currency_id', 'name'],
#         'res.partner': ['country_id'],
#     }

#     def _select(self):
#         select_str = """
#             SELECT sub.id, sub.date, sub.product_id, sub.product_name, sub.partner_id, sub.country_id, sub.account_analytic_id,
#                 sub.payment_term_id, sub.uom_name, sub.currency_id, sub.journal_id,
#                 sub.fiscal_position_id, sub.user_id, sub.company_id, sub.branch_id, sub.nbr, sub.type, sub.state,
#                 sub.categ_id, sub.date_due, sub.account_id, sub.account_line_id, sub.partner_bank_id,
#                 sub.product_qty, sub.price_total as price_total, sub.price_average as price_average,
#                 COALESCE(cr.rate, 1) as currency_rate, sub.residual as residual, sub.commercial_partner_id as commercial_partner_id
#         """
#         return select_str

#     def _sub_select(self):
#         select_str = """
#                 SELECT ail.id AS id,
#                     ai.date_invoice AS date,
#                     ail.product_id, 
#                     pt.name AS product_name, 
#                     ai.partner_id, ai.payment_term_id, ail.account_analytic_id,
#                     u2.name AS uom_name,
#                     ai.currency_id, ai.journal_id, ai.fiscal_position_id, ai.user_id, ai.company_id, ai.branch_id,
#                     1 AS nbr,
#                     ai.type, ai.state, pt.categ_id, ai.date_due, ai.account_id, ail.account_id AS account_line_id,
#                     ai.partner_bank_id,
#                     SUM ((invoice_type.sign_qty * ail.quantity) / u.factor * u2.factor) AS product_qty,
#                     SUM(ail.price_subtotal_signed * invoice_type.sign) AS price_total,
#                     SUM(ABS(ail.price_subtotal_signed)) / CASE
#                             WHEN SUM(ail.quantity / u.factor * u2.factor) <> 0::numeric
#                                THEN SUM(ail.quantity / u.factor * u2.factor)
#                                ELSE 1::numeric
#                             END AS price_average,
#                     ai.residual_company_signed / (SELECT count(*) FROM account_invoice_line l where invoice_id = ai.id) *
#                     count(*) * invoice_type.sign AS residual,
#                     ai.commercial_partner_id as commercial_partner_id,
#                     coalesce(partner.country_id, partner_ai.country_id) AS country_id
#         """
#         return select_str

#     def _from(self):
#         from_str = """
#                 FROM account_invoice_line ail
#                 JOIN account_invoice ai ON ai.id = ail.invoice_id
#                 JOIN res_partner partner ON ai.commercial_partner_id = partner.id
#                 JOIN res_partner partner_ai ON ai.partner_id = partner_ai.id
#                 LEFT JOIN product_product pr ON pr.id = ail.product_id
#                 left JOIN product_template pt ON pt.id = pr.product_tmpl_id
#                 LEFT JOIN product_uom u ON u.id = ail.uom_id
#                 LEFT JOIN product_uom u2 ON u2.id = pt.uom_id
#                 JOIN (
#                     -- Temporary table to decide if the qty should be added or retrieved (Invoice vs Credit Note)
#                     SELECT id,(CASE
#                          WHEN ai.type::text = ANY (ARRAY['in_refund'::character varying::text, 'in_invoice'::character varying::text])
#                             THEN -1
#                             ELSE 1
#                         END) AS sign,(CASE
#                          WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
#                             THEN -1
#                             ELSE 1
#                         END) AS sign_qty
#                     FROM account_invoice ai
#                 ) AS invoice_type ON invoice_type.id = ai.id
#         """
#         return from_str

#     def _group_by(self):
#         group_by_str = """
#                 GROUP BY ail.id, ail.product_id, pt.name, ail.account_analytic_id, ai.date_invoice, ai.id,
#                     ai.partner_id, ai.payment_term_id, u2.name, u2.id, ai.currency_id, ai.journal_id,
#                     ai.fiscal_position_id, ai.user_id, ai.company_id, ai.branch_id, ai.type, invoice_type.sign, ai.state, pt.categ_id,
#                     ai.date_due, ai.account_id, ail.account_id, ai.partner_bank_id, ai.residual_company_signed,
#                     ai.amount_total_company_signed, ai.commercial_partner_id, coalesce(partner.country_id, partner_ai.country_id)
#         """
#         return group_by_str

#     @api.model_cr
#     def init(self):
#         # self._table = account_invoice_report
#         tools.drop_view_if_exists(self.env.cr, self._table)
#         self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
#             WITH currency_rate AS (%s)
#             %s
#             FROM (
#                 %s %s %s
#             ) AS sub
#             LEFT JOIN currency_rate cr ON
#                 (cr.currency_id = sub.currency_id AND
#                  cr.company_id = sub.company_id AND
#                  cr.date_start <= COALESCE(sub.date, NOW()) AND
#                  (cr.date_end IS NULL OR cr.date_end > COALESCE(sub.date, NOW())))
#         )""" % (
#                     self._table, self.env['res.currency']._select_companies_rates(),
#                     self._select(), self._sub_select(), self._from(), self._group_by()))
