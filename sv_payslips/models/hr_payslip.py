# -*- coding: utf-8 -*-
import time
import babel
from openerp import fields, models,tools, api, _
from openerp.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    def get_payslip_month(self):
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.date_from, "%Y-%m-%d")))
        locale = self.env.context.get('lang') or 'en_US'
        return tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale))

    def get_payslip_lines(self):
        lines = {
            'basic' : 0.0,
            'variable' : 0.0,
            'overtime' : 0.0,
            'allowances' : 0.0,
            'other_earn' : 0.0,

            'tax' : 0.0,
            'social' : 0.0,
            'medical' : 0.0,
            'mobile' : 0.0,
            'unpaid' : 0.0,
            'other_ded' : 0.0,

            'total_ear' : 0.0,
            'total_ded' : 0.0,
            'total' : 0.0,
        }

        for line in self.line_ids:
            if line.code == 'BASIC':
                lines['basic'] += line.total

            elif line.code == 'OVT':
                lines['overtime'] += line.total

            elif line.code in ['VI']:
                lines['variable'] += line.total

            elif line.code in ['ALWS']:
                lines['allowances'] += line.total

            elif line.category_id.code in ['ALW']:
                lines['other_earn'] += line.total

            elif line.category_id.code in ['DED']:
                abs_value = abs(line.total)
                lines['total_ded'] += abs_value

                if line.code == 'INCTAX':
                    lines['tax'] += abs_value

                elif line.code == 'SIS':
                    lines['social'] += abs_value

                elif line.code in ['MIS']:
                    lines['medical'] += abs_value

                elif line.code == 'MOB':
                    lines['mobile'] += abs_value

                elif line.code == 'UNP':
                    lines['unpaid'] += abs_value

                else:
                    lines['other_ded'] += abs_value


            elif line.code == 'GROSS':
                lines['total_ear'] += line.total

            elif line.code == 'NET':
                lines['total'] += line.total

        return lines

    def convert_amount_to_text(self,amount):
        res = self.env.user.company_id.currency_id.amount_to_text(amount)
        return res

    def get_paid_date(self):
        if self.state == 'done':
            date = fields.Datetime.from_string(self.write_date)
            return date.strftime("%d-%m-%y")
        else:
            return False