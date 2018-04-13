# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SMSLog(models.Model):
    _name = 'bms.sms.log'

    name = fields.Char(string='Message')
    date = fields.Datetime()
    code = fields.Char()
    session_id = fields.Many2one('bms.session', 'Session', required=True,
                                 ondelete='cascade')
