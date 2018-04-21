# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, datetime

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools.translate import _


class BMSSession(models.Model):
    _name = 'bms.session'
    _description = 'Session'
    _inherit = ['mail.thread']
    _order = "date desc, id desc"

    @api.multi
    @api.depends('date_vn_post_send')
    def _check_warning_day(self):
        cur_date = date.today()
        for rec in self:
            if rec.date_vn_post_send and rec.document_send_type == 'vn_post':
                number_of_day = self.env['ir.config_parameter'].get_param(
                    'day.warning.miss.document', default=3)
                day_of_vn_post_send = datetime.strptime(
                    rec.date_vn_post_send, DF).date()
                number_of_date_convert = cur_date - day_of_vn_post_send
                if number_of_date_convert.days > int(number_of_day):
                    rec.warning_miss_document = True

    @api.multi
    @api.depends('product_line_ids.price_subtotal',
                 'product_line_ids.price_subtotal_tax')
    def _compute_amount_all(self):
        for session in self:
            for line in session.product_line_ids:
                session.amount_untaxed += line.price_subtotal
                session.amount_tax += line.price_subtotal_tax
            session.amount_total = session.amount_tax + session.amount_untaxed

    @api.multi
    @api.depends('user_confirm', 'manager_confirm')
    def _compute_payment_checked(self):
        for session in self:
            if session.user_confirm == 'apply' and \
                        session.manager_confirm == 'apply':
                session.payment_checked = True

    name = fields.Char(
        string='Name', required=True, default="/", readonly=True)
    code = fields.Char(string='Code', readonly=True)
    user_id = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    date = fields.Date(string='Date', default=fields.date.today())
    document_template_id = fields.Many2one(
        'bms.document.template', string='Document Template')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'bms_session_attachment_rel',
        'bms_session_id', 'attachment_id', string='Attachments',
        help='Attachments are linked to a document through model / res_id '
             'and to the message through this field.')
    attachment_ids_2 = fields.Many2many(
        'ir.attachment', 'bms_session_attachment_2_rel',
        'bms_session_id', 'attachment_id', string='Attachments',
        help='Attachments are linked to a document through model / res_id '
             'and to the message through this field.')
    document_send_type = fields.Selection(
        [('direct', 'Direct'),
         ('vn_post', 'VN Post')], string='Document Send Type',
        default='direct')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('awaiting_approval', 'Awaiting Approval'),
         ('rework', 'Re-Work'),
         ('approved', 'Approved'),
         ('vn_post', 'VN Post'),
         ('done', 'Done'),
         ('vn_post_lost', 'VN Post Lost'),
         ('vn_post_done', 'VN Post Done'),
         ('close', 'Close'),
         ('cancel', 'Cancel')], string='State', readonly=True,
        track_visibility='onchange', copy=False, default='draft')
    note = fields.Text(comodel_name='bms.document.template', string='Note',
                        related='document_template_id.description')
    note_2 = fields.Text(string='Note')
    date_vn_post_send = fields.Date(string='Date VN Post Send')
    warning_miss_document = fields.Boolean(
        string='Warning Miss Document', compute='_check_warning_day')
    mobile = fields.Char(string='Mobile',
                         default=lambda self: self.env.user.partner_id.mobile)
    email = fields.Char(string='Email',
                        default=lambda self: self.env.user.partner_id.email)
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 default=lambda self: self.env.user.partner_id)
    product_line_ids = fields.One2many('bms.session.product', 'session_id',
                                       string='Product Line')
    user_confirm = fields.Selection([
        ('draft', 'Draft'),
        ('apply', 'Apply'),
        ('cancel', 'Cancel'), ], string='User Confirm', default='draft')
    manager_confirm = fields.Selection([
        ('draft', 'Draft'),
        ('apply', 'Apply'),
        ('cancel', 'Cancel'), ], string='Manager Confirm', default='draft')
    payment_checked = fields.Boolean(string='Payment Checked',
                                     compute='_compute_payment_checked',
                                     store=True)
    amount_untaxed = fields.Float(string='Amount Untaxed',
                                  compute='_compute_amount_all', store=True)
    amount_tax = fields.Float(string='Amount Tax',
                              compute='_compute_amount_all', store=True)
    amount_total = fields.Float(string='Amount Total',
                                compute='_compute_amount_all', store=True)

    _sql_constraints = [
        ('bms_session_unique_code', 'UNIQUE (name)',
         _('The code must be unique!')),
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            name = self.env['ir.sequence'].next_by_code('bms.session')
            vals['name'] = name
            vals['code'] = 'CPDT-CASL-' + name
        return super(BMSSession, self).create(vals)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = self.env['ir.sequence'].next_by_code('bms.session')
        return super(BMSSession, self).copy(default)

    @api.multi
    def unlink(self):
        if any(self.filtered(lambda session: session.state not in (
                'draft', 'cancel', 'close'))):
            raise UserError(_(
                'You cannot delete a session '
                'which is not draft, close or cancelled!'))
        return super(BMSSession, self).unlink()

    @api.onchange('document_template_id')
    def _onchange_document_template_id(self):
        if self.document_template_id:
            attachment_ids = self.document_template_id.attachment_ids.ids
            self.attachment_ids = [(6, 0, attachment_ids)]

    @api.multi
    def action_confirm(self):
        attachment_ids = self.env['ir.attachment'].search(
            [('res_model', '=', self._name), ('res_id', '=', self.id)])
        if len(attachment_ids) != 0:
            self.state = 'awaiting_approval'
        else:
            raise UserError(_("Attach file is none"))

    @api.multi
    def action_approval(self):
        self.state = 'approved'

    @api.multi
    def action_re_work(self):
        self.state = 'rework'

    @api.multi
    def action_confirm_method_send(self):
        for rec in self:
            if rec.document_send_type == 'direct':
                rec.state = 'done'
            else:
                rec.state = 'vn_post'
                rec.date_vn_post_send = date.today()

    @api.multi
    def action_mark_received_document(self):
        self.state = 'vn_post_done'

    @api.multi
    def action_mark_lost_document(self):
        self.state = 'vn_post_lost'

    @api.multi
    def action_mark_done(self):
        self.state = 'done'

    @api.multi
    def action_mark_close(self):
        self.state = 'close'

    @api.multi
    def user_confirmed(self):
        for record in self:
            record.user_confirm = 'apply'

    @api.multi
    def user_unconfirmed(self):
        for record in self:
            record.user_confirm = 'cancel'

    @api.multi
    def manager_confirmed(self):
        for record in self:
            record.manager_confirm = 'apply'

    @api.multi
    def manager_unconfirmed(self):
        for record in self:
            record.manager_confirm = 'cancel'

    @api.multi
    def payment_online(self):
        return


class BMSSessionProduct(models.Model):
    _name = 'bms.session.product'

    @api.multi
    @api.depends('quantity', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.quantity
            line.price_subtotal_tax = line.price_subtotal * line.tax / 100

    name = fields.Char(string='Note')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    code = fields.Char(string='Code')
    price_unit = fields.Float(string='Price')
    tax = fields.Float(string='Tax (%)')
    price_subtotal = fields.Float(string='Price Subtotal',
                                  compute='_compute_amount', store=True)
    price_subtotal_tax = fields.Float(string='Price Subtotal Tax',
                                      compute='_compute_amount', store=True)
    session_id = fields.Many2one('bms.session', string='Session',
                                 ondelete='cascade')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.code = self.product_id.default_code
            self.price_unit = self.product_id.lst_price
            self.quantity = 1
