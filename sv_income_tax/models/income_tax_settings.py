# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def call_income_tax(self,gross):
        print("opopopopopo" , gross)
        res = 0
        res = self.env['income.tax.settings'].calc_income_tax(gross)
        return res


class IncomeTaxSettings(models.Model):
    _name = 'income.tax.settings'

    # max_seq = fields.Integer(string="", required=False, )
    name = fields.Char(string="Name", required=False, )
    line_ids = fields.One2many(comodel_name="income.tax.settings.line", inverse_name="income_tax_id", string="Taxes Divisions", required=False,ondelete='cascade' )
    is_functional_exempt = fields.Boolean(string="Function Exemption",  )
    functional_exempt_value = fields.Float(string="Functional Exemption Value",  required=False, store=True)

    @api.constrains('line_ids')
    def check_line_ids(self):
        if self.line_ids:
            prev = self.line_ids[0].max_value
            for line in self.line_ids[1:]:
                if abs(prev - line.min_value) > 0.0001:
                    raise ValidationError('Tax Division Is Missing')
                prev = line.max_value

    @api.multi
    def calc_income_tax(self,tax_pool):
        income_tax_settings = self.env.ref('sv_income_tax.income_tax_settings0')
        functional_exemption = income_tax_settings.is_functional_exempt and income_tax_settings.functional_exempt_value or 0
        print(tax_pool , functional_exemption , "functional_exemptionfunctional_exemptionfunctional_exemption")

        effective_salary = tax_pool - functional_exemption
        # effective_salary = tax_pool
        print(effective_salary , "effective_salaryeffective_salaryeffective_salaryeffective_salaryeffective_salary")
        income_tax = 0
        income_tax_after_exemption = 0
        for line in income_tax_settings.line_ids:
            if line.diff_value:
                if 0 < effective_salary <= line.diff_value:
                    income_tax += (line.tax_ratio / 100.0) * effective_salary
                    income_tax_after_exemption = (100 - line.discount_ratio) / 100.0 * income_tax
                    break
                elif effective_salary > line.diff_value:
                    effective_salary -= line.diff_value
                    income_tax += (line.tax_ratio / 100.0) * line.diff_value
            else:
                income_tax += (line.tax_ratio / 100.0) * effective_salary
                break
        return income_tax_after_exemption

class IncomeTaxSettingsLine(models.Model):
    _name = 'income.tax.settings.line'
    _order = 'min_value asc'

    income_tax_id = fields.Many2one(comodel_name="income.tax.settings", string="Income Tax Settings", required=False, )
    max_value = fields.Float(string="Maximum Value",  required=False,)
    diff_value = fields.Float(string="Difference Value",  required=False,compute='compute_diff_value' )
    tax_ratio = fields.Float(string="Tax Ratio %",  required=False, )
    discount_ratio = fields.Float(string="Discount Ratio %",  required=False, )

    sequence = fields.Integer(string="Sequence", required=False)
    min_value = fields.Float(string="Minimum Value",  required=False )


    @api.multi
    @api.depends('max_value','max_value')
    def compute_diff_value(self):
        for rec in self:
            if rec.max_value:
                rec.diff_value = rec.max_value - rec.min_value

    @api.constrains('max_value','max_value','discount_ratio','tax_ratio')
    def check_all_values(self):
        if self.max_value and self.min_value and self.max_value < self.min_value:
            raise ValidationError('Minimum Value Can not be greater than maximum value')
        if self.tax_ratio < 0 or self.tax_ratio > 100:
            raise ValidationError('Tax Ratio Must Be Between 0 and 100')
        if self.discount_ratio < 0 or self.discount_ratio > 100:
            raise ValidationError('Discount Ratio Must Be Between 0 and 100')
        rec = self.search([('sequence','=',self.sequence)])
        if len(rec) > 1:
            raise ValidationError('sequence can not be repeated')




