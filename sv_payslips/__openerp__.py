{
    'name':'PAYSLIPS',
    'author':'ahmed yousef',
    'data':[
        # 'security/ir.model.access.csv',
        'views/hr_contract.xml',
        # 'views/mobile_bill.xml',
        # 'views/hr_payslip.xml',
        # 'report/hr_payslip_report.xml',
        'data/data.xml',
        'data/salary_rules.xml',
    ],

   'depends': ['hr','hr_contract','hr_payroll'],
}