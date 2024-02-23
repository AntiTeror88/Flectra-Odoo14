# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    market_place_id = fields.Many2one(comodel_name="market.place", string="Market", readonly=True)
    slabel = fields.Char('Label', readonly=True)

    # pylint:disable=dangerous-default-value
    def _query(
        self, with_clause="", fields={}, groupby="", from_clause=""  # noqa: B006
    ):
        fields["market_place_id"] = ", s.sale_marketplace as market_place_id"
        fields["slabel"] = ",l.name as slabel"
        groupby += ", s.sale_marketplace, l.name"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
