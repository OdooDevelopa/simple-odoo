# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
import unicodedata

from odoo import api, fields, models
from odoo.tools.translate import _


class BMSSmsTemplateConfig(models.Model):
    _name = 'bms.sms.template.config'
    _description = 'Sms Template Config'
    _inherit = 'bms.session'

    stc_name = fields.Char(string='Name')
    actived = fields.Boolean(string='Active')
    sms_template = fields.Many2one('mail.template')
    _sql_constraints = [
        ('bms_sms_template_config_state', 'UNIQUE (state)',
         _('The state must be unique!')),
    ]

    def send_sms(self, session_id):
        if not self.sms_template:
            return
        if not self.actived:
            return
        self.sms_template.send_sms(session_id)


class BMSMailTemplate(models.Model):
    _inherit = 'mail.template'

    @api.multi
    def send_sms(self, session_id):
        values = self.generate_email(session_id)
        content = self.no_accent_vietnamese(values['body'])
        telephone = self.env['bms.session'].browse(
            session_id).partner_id.mobile
        self.env['bms.sms.compose'].create({
            'to_number': telephone,
            'message': content,
            'session_id': session_id
        }).send_entity()
        return True

    @api.model
    def no_accent_vietnamese(self, s):
        s = re.compile(r"[\s]+").sub(" ", s)
        s = re.compile(r"</?(p|div|br).*?>", re.IGNORECASE | re.DOTALL).sub(
            "\n", s)
        s = re.compile(r"<.*?>", re.DOTALL).sub("", s)
        s = re.compile("[^\S\n]+", re.UNICODE).sub(" ", s)
        s = re.compile("(\n )").sub("\n", s)
        s = re.compile("\n\n+").sub("\n\n", s)
        s = s.strip()
        # s = s.decode('utf-8')
        s = re.sub(u'Đ', 'D', s)
        s = re.sub(u'đ', 'd', s)
        return unicodedata.normalize(
            'NFKD', unicode(s)).encode('ASCII', 'ignore')
