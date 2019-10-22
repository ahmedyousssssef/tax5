# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.one
    def _compute_work_hour_value(self):
        """
            calculate total working hours
        """
        if self.month_workdays == 0 or self.workday_hours == 0:
            self.work_hour_value = 0
        else:
            self.work_hour_value = round((self.wage + self.variable_salary + self.allowances + self.other_earnings ) / self.month_workdays / self.workday_hours, 2)
    # company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    #
    # currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    wage = fields.Float('Basic Salary', digits=(16, 2), required=True, help="Employee's monthly gross wage.")
    variable_salary = fields.Float(string="Variable Salary")
    allowances = fields.Float(string="Allowances",  required=False, )
    other_earnings = fields.Float(string="Other Earnings",  required=False, )
    fixed_insurance = fields.Float(string="Fixed Insurance Amount",  required=False, )
    variable_insurance = fields.Float(string="Variable Insurance Amount",  required=False, )
    medical_insurance = fields.Float(string="Medical Insurance",  required=False, )
    mobile = fields.Float(string="Mobile",  required=False, )

    # fixed_insurance_ratio = fields.Float(string="Fixed Insurance Percentage(%)",default=14,  required=False, )
    # variable_insurance_ratio = fields.Float(string="Variable Insurance Percentage(%)",default=11,  required=False, )
    monthly_insurance_subscription = fields.Float(string="Monthly Insurance Subscription")
    work_hour_value = fields.Float(compute=_compute_work_hour_value,
                                   string='Work Hour Value', readonly=True)
    job_nature = fields.Float(string="Job Nature",  required=False, )

    # @api.multi
    # @api.onchange('wage','fixed_insurance_ratio')
    # def compute_fixed_insurance(self):
    #
    #     for record in self :
    #         if record.wage:
    #             record.fixed_insurance = (record.fixed_insurance_ratio/100.0) * record.wage
    #
    # @api.multi
    # @api.onchange('variable_salary','allowances','variable_insurance_ratio')
    # def compute_variable_insurance(self):
    #     for record in self :
    #
    #         record.variable_insurance = (record.variable_insurance_ratio/100.0)*(record.variable_salary)
    #
    #
    # @api.onchange('fixed_insurance','variable_insurance')
    # def onchange_insurance(self):
    #     self.update({'monthly_insurance_subscription':self.fixed_insurance + self.variable_insurance })
    #
