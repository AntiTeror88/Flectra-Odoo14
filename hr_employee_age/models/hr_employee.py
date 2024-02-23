# Copyright (C) 2015 Salton Massally (<smassally@idtlabs.sl>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # first_contract_date = fields.Date(string='first contract date',store=True,)
    age = fields.Integer(tring='Age',compute="_compute_age",store=True,)
    contract_period = fields.Integer(string='Contract Period',compute="_compute_contract_period",readonly=True, store=True,)



    @api.depends("birthday")
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthday:
                age = relativedelta(fields.Date.today(), record.birthday).years
            record.age = age


    @api.depends("first_contract_date")
    def _compute_contract_period(self):
        for record in self:
            contract_period = 0
            if record.first_contract_date:
                contract_period = relativedelta(fields.Date.today(), record.first_contract_date).years
            record.contract_period = contract_period