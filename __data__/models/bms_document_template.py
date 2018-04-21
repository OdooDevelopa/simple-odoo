# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BMSDocumentTemplateCategory(models.Model):
    _name = 'bms.document.template.category'
    _description = 'Document Template Category'

    name = fields.Char(string='Name')
    parent_id = fields.Many2one(
        'bms.document.template.category', string='Parent')


class BMSDocumentTemplate(models.Model):
    _name = 'bms.document.template'
    _description = 'Document Template'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    category_id = fields.Many2one(
        'bms.document.template.category', string='Category')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'bms_document_tmpl_attachment_rel',
        'bms_document_tmpl_id', 'attachment_id', string='Attachments',
        help='Attachments are linked to a document through model / res_id '
             'and to the message through this field.')
    description = fields.Text(string='Description')
    user_id = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user)
