# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging
import re
import urllib
from datetime import datetime

import werkzeug.exceptions

from odoo import api, exceptions, fields, models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
p = '^\+?\d{1,3}?[- .]?\(?(?:\d{2,3})\)?[- .]?\d\d\d[- .]?\d\d\d\d$'

try:
    import requests
except ImportError:
    _logger.warn('Cannot `import requests`.')


class SMSCompose(models.TransientModel):
    _name = "bms.sms.compose"

    to_number = fields.Char()
    message = fields.Char()
    session_id = fields.Many2one('bms.session', string='Session')

    @api.multi
    @api.constrains('to_number')
    def _check_phone_number(self):
        for rec in self:
            if rec.to_number and not re.match(p, rec.to_number):
                raise exceptions.ValidationError(_(
                    'The mobile number is not available'))
        return True

    @api.multi
    @api.constrains('message')
    def _check_message_ascii(self):
        for rec in self:
            is_ascii = all(ord(char) < 128 for char in rec.message)
            if not is_ascii:
                raise exceptions.ValidationError(_(
                    'The content of message is invalid'))
        return True

    @api.multi
    def send_entity(self):
        config = self.env['bms.sms.config'].search([])
        sms_log = self.env['bms.sms.log']
        if config:
            values = {'username': config.username,
                      'password': config.password,
                      'source_addr': config.brand_name,
                      'dest_addr': self._check_mobile(self.to_number),
                      'message': self.message}
            ary_ordered_names = []
            ary_ordered_names.append('username')
            ary_ordered_names.append('password')
            ary_ordered_names.append('source_addr')
            ary_ordered_names.append('dest_addr')
            ary_ordered_names.append('message')
            postdata = "&".join(
                [item + '=' + urllib.quote_plus(values[item]) for item in
                 ary_ordered_names])
            if requests:
                try:
                    response_string = requests.get(config.url + '?' + postdata)
                    if response_string:
                        code = response_string.text.encode('utf-8')
                        sms_log.create({
                            'session_id': self.session_id.id,
                            'name': self.message,
                            'date': datetime.now(),
                            'code': code
                        })
                except requests.exceptions.RequestException as exception:
                    return self._make_error_response(
                        exception.response.status_code,
                        exception.response.reason or _("Unknown Error"))

    def _make_error_response(self, status, message):
        exception = werkzeug.exceptions.HTTPException()
        exception.code = status
        exception.description = message
        return exception

    def _check_mobile(self, mobile):
        if mobile:
            mobile_prefix = '84'
            if mobile.startswith("0"):
                mobile = mobile_prefix + mobile[1:].replace(" ", "")
            elif mobile.startswith("+"):
                mobile = mobile.replace("+", "")
            else:
                mobile = mobile.replace(" ", "")
        return mobile
