# -*- coding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json
import logging
import pprint
import urllib2
import werkzeug

from openerp import http, SUPERUSER_ID
from openerp.http import request

_logger = logging.getLogger(__name__)


class VoguePayController(http.Controller):
    _notify_url = '/payment/voguepay/ipn/'
    _return_url = '/payment/voguepay/dpn/'
    _cancel_url = '/payment/voguepay/cancel/'

    def _get_return_url(self, **post):
        """ Extract the return URL from the data coming from voguepay. """
        return_url = post.pop('return_url', '')
        if not return_url:
            custom = json.loads(post.pop('custom', '{}'))
            return_url = custom.get('return_url', '/')
        return return_url

    def voguepay_validate_data(self, **post):
        """ VoguePay IPN: three steps validation to ensure data correctness

         - step 1: return an empty HTTP 200 response -> will be done at the end
           by returning ''
         - step 2: POST the complete, unaltered message back to VoguePay (preceded
           by cmd=_notify-validate), with same encoding
         - step 3: voguepay send either VERIFIED or INVALID (single word)

        Once data is validated, process it. """
        res = False
        new_post = dict(post, cmd='_notify-validate')
        urequest = urllib2.Request("https://www.sandbox.voguepay.com/cgi-bin/webscr", werkzeug.url_encode(new_post))
        uopen = urllib2.urlopen(urequest)
        resp = uopen.read()
        if resp == 'VERIFIED':
            _logger.info('VoguePay: validated data')
            cr, uid, context = request.cr, SUPERUSER_ID, request.context
            res = request.registry['payment.transaction'].form_feedback(cr, uid, post, 'voguepay', context=context)
        elif resp == 'INVALID':
            _logger.warning('VoguePay: answered INVALID on data verification')
        else:
            _logger.warning('VoguePay: unrecognized voguepay answer, received %s instead of VERIFIED or INVALID' % resp.text)
        return res

    @http.route('/payment/voguepay/ipn/', type='http', auth='none', methods=['POST'])
    def voguepay_ipn(self, **post):
        """ VoguePay IPN. """
        _logger.info('Beginning VoguePay IPN form_feedback with post data %s', pprint.pformat(post))  # debug
        self.voguepay_validate_data(**post)
        return ''

    @http.route('/payment/voguepay/dpn', type='http', auth="none", methods=['POST'])
    def voguepay_dpn(self, **post):
        """ VoguePay DPN """
        _logger.info('Beginning VoguePay DPN form_feedback with post data %s', pprint.pformat(post))  # debug
        return_url = self._get_return_url(**post)
        self.voguepay_validate_data(**post)
        return werkzeug.utils.redirect(return_url)

    @http.route('/payment/voguepay/cancel', type='http', auth="none")
    def voguepay_cancel(self, **post):
        """ When the user cancels its VoguePay payment: GET on this route """
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        _logger.info('Beginning VoguePay cancel with post data %s', pprint.pformat(post))  # debug
        return_url = self._get_return_url(**post)
        return werkzeug.utils.redirect(return_url)
