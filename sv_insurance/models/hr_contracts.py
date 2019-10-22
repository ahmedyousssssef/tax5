# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)

class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def get_insurance_primary_wage(self,date_from=None,date_to=None):
        # date_from_o = fields.Date.from_string(date_from)
        contract_start_date_o = fields.Date.from_string(self.date_start)
        if contract_start_date_o.month > 7:
            insurance_year = self.env['hr.insurance.year'].search([('year','=',str(contract_start_date_o.year)),('type','=','fixed')],limit=1)
            if insurance_year:
                return insurance_year.insurance_amount
            else:
                insurance_year = self.env['hr.insurance.year'].search([('type','=','fixed'),('year','<',str(contract_start_date_o.year))],order="year desc",limit=1)
                return insurance_year.insurance_amount if insurance_year.insurance_amount else 1370
        else:
            insurance_year = self.env['hr.insurance.year'].search([('year','=',str(contract_start_date_o.year - 1)),('type','=','fixed')],limit=1)
            if insurance_year:
                return insurance_year.insurance_amount
            else:
                insurance_year = self.env['hr.insurance.year'].search([('type','=','fixed'),('year','<',str(contract_start_date_o.year-1))],order="year desc",limit=1)
                primary_insurance = insurance_year.insurance_amount if insurance_year else 1370
                return primary_insurance

    @api.multi
    def get_insurance_variable_wage(self,date_from,date_to=None):
        date_from_o = fields.Date.from_string(date_from)
        insurance_variable = self.env['hr.insurance.year'].search(
            [('year', '=', str(date_from_o.year)), ('type', '=', 'variable')], limit=1)
        if not insurance_variable:
            insurance_variable = self.env['hr.insurance.year'].search([('type', '=', 'variable')],order="year desc", limit=1)
        variable_insurance_limit = insurance_variable and insurance_variable.insurance_amount or 2800
        # primary_insurance = self.get_insurance_primary_wage(date_from,date_to)
        variable_insurance = min((self.variable_salary),variable_insurance_limit)
        return variable_insurance



