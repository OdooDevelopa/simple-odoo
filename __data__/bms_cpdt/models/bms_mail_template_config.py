# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools.translate import _


class BMSMailTemplateConfig(models.Model):
    _name = 'bms.mail.template.config'
    _description = 'Mail Template Config'
    _inherit = 'bms.session'

    mtc_name = fields.Char()
    actived = fields.Boolean(string="Active")
    mail_template = fields.Many2one(comodel_name="mail.template")
    _sql_constraints = [
        ('bms_mail_template_config_state', 'UNIQUE (state)',
         _('The state must be unique!')),
    ]

    def send_mail(self, session_id, force_send=False):
        if not self.mail_template:
            return
        if not self.actived:
            return
        self.mail_template.send_mail(session_id, force_send)
