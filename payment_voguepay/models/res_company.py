# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class ResCompany(osv.Model):
    _inherit = "res.company"

    def _get_voguepay_account(self, cr, uid, ids, name, arg, context=None):
        Acquirer = self.pool['payment.acquirer']
        company_id = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id.id
        voguepay_ids = Acquirer.search(cr, uid, [
            ('website_published', '=', True),
            ('name', 'ilike', 'voguepay'),
            ('company_id', '=', company_id),
        ], limit=1, context=context)
        if voguepay_ids:
            voguepay = Acquirer.browse(cr, uid, voguepay_ids[0], context=context)
            return dict.fromkeys(ids, voguepay.voguepay_email_account)
        return dict.fromkeys(ids, False)

    def _set_voguepay_account(self, cr, uid, id, name, value, arg, context=None):
        Acquirer = self.pool['payment.acquirer']
        company_id = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id.id
        voguepay_account = self.browse(cr, uid, id, context=context).voguepay_account
        voguepay_ids = Acquirer.search(cr, uid, [
            ('website_published', '=', True),
            ('voguepay_email_account', '=', voguepay_account),
            ('company_id', '=', company_id),
        ], context=context)
        if voguepay_ids:
            Acquirer.write(cr, uid, voguepay_ids, {'voguepay_email_account': value}, context=context)
        return True

    _columns = {
        'voguepay_account': fields.function(
            _get_voguepay_account,
            fnct_inv=_set_voguepay_account,
            nodrop=True,
            type='char', string='VoguePay Account',
            help="VoguePay username (usually email) for receiving online payments."
        ),
    }
