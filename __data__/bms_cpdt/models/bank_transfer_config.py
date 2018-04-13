# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BankTransferConfig(models.Model):
    _name = 'bank.transfer.config'
    _description = 'Bank transfer config'
    _inherit = ['mail.thread']

    name = fields.Char(string='Content', required=True)
