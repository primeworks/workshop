# -*- coding: utf-8 -*-

{
    'name': 'VoguePay Payment Acquirer',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: VoguePay Implementation',
    'version': '1.0',
    'description': """VoguePay Payment Acquirer""",
    'author': 'OpenERP SA',
    'depends': ['payment'],
    'data': [
        'views/voguepay.xml',
        'views/payment_acquirer.xml',
        'views/res_config_view.xml',
        'data/voguepay.xml',
    ],
    'installable': True,
}
