# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)



class HrInsuranceYear(models.Model):
    _name = 'hr.insurance.year'
    _rec_name = 'name'
    _description = 'Insurance Amounts By Year'
    _order = 'name asc, id desc'



    def _default_year(self):
        today = datetime.today()
        current_year = today.year
        return str(current_year)

    def _get_year_selection(self):
        _year_selection = [('2015', '2015'), ('2016', '2016'), ('2017', '2017')]
        today = datetime.today()
        current_year = today.year
        year = current_year
        # year = current_year + 1
        while year > 2017:
            _year_selection.append((str(year),str(year)))
            year -= 1
        return _year_selection

    name = fields.Char(string="Name", required=False, )
    insurance_amount = fields.Float(string="Max Limit",  required=False, )
    year = fields.Selection(string="Year", selection=_get_year_selection,default=_default_year, required=False, )
    type = fields.Selection(string="Insurance Wage Type", selection=[('fixed', 'Fixed Insurance Limit'), ('variable', 'Variable Insurance Limit')], required=False, )
    employee_ratio = fields.Float(string="Employee Ratio (%)",  required=False, )
    company_ratio = fields.Float(string="Company Ration (%)",  required=False, )

    @api.multi
    def unlink(self):
        raise ValidationError('You Can not delete Insurance Wage')

    @api.constrains('year','type')
    def _check_year(self):
        if self.search_count([('year','=',self.year),('type','=',self.type)]) > 1:
            raise ValidationError('Salary Insurance Can not be Set Twice Per Year For the same type')

    @api.constrains('employee_ratio','company_ratio')
    def check_ratios(self):
        if  not (0 < self.employee_ratio < 100):
            raise ValidationError('Employee ratio must be between 0% and 100%')
        if  not (0 < self.company_ratio < 100):
            raise ValidationError('Company ratio must be between 0% and 100%')

    @api.onchange('type')
    def onchange_type(self):
        if self.type == 'fixed':
            self.update({
                'employee_ratio':14.0,
                'company_ratio':26.0,
            })

        elif self.type == 'variable':
            self.update({
                'employee_ratio':11.0,
                'company_ratio':24.0,
            })