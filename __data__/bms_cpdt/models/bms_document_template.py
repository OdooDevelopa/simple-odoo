# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BMSDocumentTemplateCategory(models.Model):
    _name = 'bms.document.template.category'
    _description = 'Document Template Category'

    name = fields.Char()
    parent_id = fields.Many2one(
        'bms.document.template.category', string='Parent')
    template_ids = fields.One2many('bms.document.template',
                                   'tmpl_category_id',
                                   'Templates')


class BMSDocumentTemplate(models.Model):
    _name = 'bms.document.template'
    _description = 'Document Template'

    name = fields.Char()
    active = fields.Boolean(default=True)
    tmpl_category_id = fields.Many2one('bms.document.template.category',
                                       string='Template Category')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'bms_document_tmpl_attachment_rel',
        'bms_document_tmpl_id', 'attachment_id', string='Attachments',
        help='Attachments are linked to a document through model / res_id '
             'and to the message through this field.')

    attachment_papers = fields.Many2many(
        'bms.papers.template', 'bms_document_tmpl_attachment_papers_rel',
        'bms_document_tmpl_id', 'attachment_paper', string='Attachments',
        help='Attachments are linked to a document through model / res_id '
             'and to the message through this field.')

    note = fields.Text()
    show_note_on_website = fields.Boolean(
        compute='_compute_show_note_on_website')
    user_id = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user)
    description = fields.Html()
    purpose_scope_content = fields.Html(
        string='Purpose / scope / content of the process')
    legal_basic_ids = fields.Many2many(
        'bms.legal.basic', 'bms_document_tmpl_legal_basic_rel',
        'bms_document_tmpl_id', 'bms_legal_basic_id', string="Legal basic",
        help='Relevant legal basis')
    faq = fields.Html()
    department_id = fields.Many2one('hr.department',
                                    string='Police department')

    @api.multi
    def _compute_show_note_on_website(self):
        for template in self:
            if template.note and template.note.lower().strip() == u'không có':
                template.show_note_on_website = False
                continue
            template.show_note_on_website = True

    @api.model
    def create(self, vals):
        if 'attachment_ids' in vals:
            if len(vals['attachment_ids']) > 0:
                list_attachment = vals['attachment_ids'][0][2]
                for at in list_attachment:
                    self.env['ir.attachment'].browse(
                        at).write({'public': True})
        return super(BMSDocumentTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'attachment_ids' in vals:
            list_attachment = vals['attachment_ids'][0][2]
            for at in list_attachment:
                self.env['ir.attachment'].browse(at).write({'public': True})
        return super(BMSDocumentTemplate, self).write(vals)
