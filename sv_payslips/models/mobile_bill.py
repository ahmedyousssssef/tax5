# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class MobileBill(models.Model):
    _name = 'mobile.bill'

    name = fields.Char(string="Name", required=False, )
    date_from = fields.Date(string="Date From", default=lambda self:self.default_date_from() )
    date_to = fields.Date(string="Date To",default=lambda self:self.default_date_to())
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", default=lambda self:self.env.user.company_id.currency_id)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=False, )
    amount = fields.Monetary(string="Amount",  required=False, )
    state = fields.Selection(string="", selection=[('draft', 'Draft'), ('done', 'Done'), ], default='draft' )

    @api.model
    def create(self,vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mobile.bill')
        return super(MobileBill,self).create(vals)

    @api.multi
    def action_done(self):
        for rec in self:
            rec.write({'state':'done'})

    def default_date_from(self):
        date_now = datetime.now()
        start_current_month = date_now.replace(day=1)
        start_previous_month = start_current_month + relativedelta(months=-1)
        return str(start_previous_month.date())

    def default_date_to(self):
        date_now = datetime.now()
        start_current_month = date_now.replace(day=1)
        end_previous_month = start_current_month + relativedelta(days=-1)
        return str(end_previous_month.date())