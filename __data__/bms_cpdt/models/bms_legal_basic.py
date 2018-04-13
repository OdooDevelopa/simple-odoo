# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class BMSLegalBasic(models.Model):
    _name = 'bms.legal.basic'
    _description = 'Legal basic'
    _rec_name = 'id'

    name = fields.Char(required=True)
    content = fields.Html()
    note = fields.Text()
    attachment_ids = fields.Many2many(
        'ir.attachment', 'bms_legal_basic_attachment_rel',
        'bms_legal_basic_id', 'attachment_id', string='Attachments',
        help='Attachments are linked to a document through model / res_id '
             'and to the message through this field.')

    @api.model
    def create(self, vals):
        LegalBasic = super(BMSLegalBasic, self).create(vals)
        if 'attachment_ids' in vals:
            if len(vals['attachment_ids']) > 0:
                list_attachment = vals['attachment_ids'][0][2]
                if len(list_attachment) > 0:
                    for at in list_attachment:
                        self.env['ir.attachment'] \
                            .browse(at).write({'public': True})
        return LegalBasic

    @api.multi
    def write(self, vals):
        if 'attachment_ids' in vals:
            list_attachment = vals['attachment_ids'][0][2]
            for at in list_attachment:
                self.env['ir.attachment'].browse(at).write({'public': True})
        LegalBasic = super(BMSLegalBasic, self).write(vals)
        return LegalBasic
