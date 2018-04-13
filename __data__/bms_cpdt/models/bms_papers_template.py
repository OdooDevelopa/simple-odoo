# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BMSPapersTemplate(models.Model):
    _name = 'bms.papers.template'
    _inherits = {'ir.attachment': 'attachment_id'}
    _description = 'Papers Template'

    attachment_id = fields.Many2one('ir.attachment', string='Attachment',
                                    required=True, ondelete='cascade')
