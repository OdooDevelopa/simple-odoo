# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import date, datetime

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class BMSSession(models.Model):
    _name = 'bms.session'
    _description = 'Session'
    _inherit = ['mail.thread']
    _order = "date desc, id desc"

    def send_email_and_sms(self):
        self.env['bms.mail.template.config'] \
            .search([('state', '=', self.state)]) \
            .send_mail(self.id)
        if self.receive_doc_via_sms:
            self.env['bms.sms.template.config'] \
                .search([('state', '=', self.state)]) \
                .send_sms(self.id)

    @api.multi
    def schedule_meeting(self):
        partner_ids = [self.partner_id.id]
        partner_ids.append(self.env.user.partner_id.id)
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        action['context'] = {
            'search_default_partner_ids': self._context['partner_name'],
            'default_partner_ids': partner_ids,
        }
        return action

    @api.model
    def get_dmain_man(self):
        cpdt_manager = self.env.ref('bms_cpdt.group_e_gov_manager')
        return [('id', 'in', cpdt_manager.users.ids)]

    @api.model
    def check_document_automatically(self):
        for session in self.env['bms.session'].search([]):
            # Check document is missing or not then send an email to notify
            if (session.warning_miss_document and
                    not session.lostdoc_email_sent):
                session.write({'state': 'vn_post_lost',
                               'lostdoc_email_sent': True, })
                session.send_email_and_sms()
            # Check document state is done or not to change to 'Close'
            if session.state == 'done':
                session.write({'state': 'close'})
                session.send_email_and_sms()

    @api.multi
    @api.depends('date_vn_post_send')
    def _compute_check_warning_day(self):
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
            if session.user_confirm == session.manager_confirm == 'apply':
                session.payment_checked = True

    @api.multi
    def _compute_name(self):
        for session in self:
            session.name2 = session.name

    @api.model
    def get_name_default(self):
        res = self.env['ir.sequence'].next_by_code('bms.session')
        return res

    @api.model
    def default_get(self, fields_list):
        res = super(BMSSession, self).default_get(fields_list)
        if 'name' not in fields_list:
            return res
        name = self.get_name_default()
        res['name'] = name
        res['name2'] = name
        return res

    @api.model
    def _default_bank_transfer_config(self):
        bank_transfer_config = \
            self.sudo().env.ref('bms_cpdt.bank_transfer_config_record').name
        return bank_transfer_config

    # name = fields.Char(required=True, default="/", readonly=True)
    name = fields.Char(required=True)
    name2 = fields.Char(compute='_compute_name', readonly=True)
    code = fields.Char(readonly=True)
    user_id = fields.Many2one(
        'res.users', default=lambda self: self.env.user)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)
    date = fields.Date(default=fields.date.today())
    document_template_ids = fields.Many2many(
        'bms.document.template', 'bms_session_document_template_rel',
        'bms_session_id', 'document_template_id',
        string='Document template', required=True)
    attachment_ids = fields.Many2many(
        'ir.attachment', 'bms_session_attachment_rel',
        'bms_session_id', 'attachment_id', string='Attachments',
        help='Attachments are linked to a document through model / res_id '
             'and to the message through this field.')
    attachment_papers_ids = fields.One2many('bms.session.attachment',
                                            'session_id',
                                            string='Attachment Paper Line')
    attachment_ids_2 = fields.Many2many(
        'ir.attachment', 'bms_session_attachment_2_rel',
        'bms_session_id', 'attachment_id', string='Attachments',
        help='Attachments are linked to a document through model / res_id '
             'and to the message through this field.')
    document_send_type = fields.Selection(
        [('direct', 'Direct'),
         ('vn_post', 'VN Post')], default='direct')
    document_receive_type = fields.Selection(
        [('direct', 'Direct'),
         ('vn_post', 'VN Post')], default='direct')
    receive_doc_via_sms = fields.Boolean(string="Receive via SMS")
    profile_received = fields.Boolean()
    payment = fields.Boolean(string='Money Received')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('awaiting_approval', 'Awaiting Approval'),
         ('rework', 'Re-Work'),
         ('approved', 'Approved'),
         ('vn_post_check', 'Check profile'),
         ('missing_profile', 'Missing profile'),
         ('result_profile_returned', 'Result profile returned'),
         ('result_profile_sent', 'Result profile sent'),
         ('done', 'Done'),
         ('vn_post_lost', 'VN Post Lost'),
         ('vn_post_done', 'VN Post Done'),
         ('close', 'Close'),
         ('cancel', 'Cancel')], readonly=True,
        track_visibility='onchange', copy=False, default='draft')
    lostdoc_email_sent = fields.Boolean(string="Is lostdoc email sent")
    note = fields.Text()
    note_2 = fields.Text(string='Note')
    description = fields.Text()
    date_vn_post_send = fields.Date(string='Date VN Post Send')
    warning_miss_document = fields.Boolean(
        compute='_compute_check_warning_day')
    mobile = fields.Char(default=lambda self: self.env.user.partner_id.mobile)
    email = fields.Char(default=lambda self: self.env.user.partner_id.email)
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 default=lambda self: self.env.user.partner_id)
    product_line_ids = fields.One2many('bms.session.product', 'session_id',
                                       string='Product Line')
    user_confirm = fields.Selection([
        ('draft', 'Draft'),
        ('apply', 'Apply'),
        ('cancel', 'Cancel'), ], default='draft')
    manager_confirm = fields.Selection([
        ('draft', 'Draft'),
        ('apply', 'Apply'),
        ('cancel', 'Cancel'), ], default='draft')
    payment_checked = fields.Boolean(
        compute='_compute_payment_checked', store=True)
    amount_untaxed = fields.Float(compute='_compute_amount_all', store=True)
    amount_tax = fields.Float(compute='_compute_amount_all', store=True)
    amount_total = fields.Float(compute='_compute_amount_all', store=True)
    department_id = fields.Many2one('hr.department', string='Department')
    handler = fields.Many2one(
        "res.users", string="Handler manager", domain=get_dmain_man)
    # sms_log_ids = fields.One2many(
    #     'bms.sms.log', 'session_id', string='SMS Log')
    payment_status = fields.Selection(
        [('unpaid', 'Unpaid'),
         ('paid', 'Paid')], default='unpaid')
    type = fields.Selection([('normal', 'Normal'),
                             ('send_a_copy', 'Send a copy')],
                            default='normal', readonly=True)
    next_sequence = fields.Integer(compute='_compute_next_sequence',
                                   default=1)
    bank_transfer_config = fields.Char(compute='_compute_bank_transfer_config',
                                       default=_default_bank_transfer_config)

    _sql_constraints = [
        ('bms_session_unique_code', 'UNIQUE (name)',
         _('The code must be unique!')),
    ]

    @api.multi
    @api.constrains('document_template_ids')
    def _check_document_template_ids(self):
        for session in self:
            if not session.document_template_ids:
                raise exceptions.ValidationError(_(
                    'You must enterd request settlement!'))
        return True

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

    @api.multi
    def _compute_bank_transfer_config(self):
        bank_transfer_config = self._default_bank_transfer_config()
        for session in self:
            session.bank_transfer_config = bank_transfer_config

    @api.multi
    def _compute_next_sequence(self):
        for session in self:
            next_sequence = 0
            for line in session.product_line_ids:
                if line.sequence > next_sequence:
                    next_sequence = line.sequence
            session.next_sequence = next_sequence + 1

    @api.onchange('product_line_ids')
    def product_line_change(self):
        next_sequence = 0
        for line in self.product_line_ids:
            if line.sequence > next_sequence:
                next_sequence = line.sequence
        next_sequence += 1
        self.next_sequence = next_sequence

    # @api.onchange('document_template_ids')
    # def _onchange_document_template_id(self):
    #     attachment_ids = []
    #     description = note = ''
    #     for tmpl in self.document_template_ids:
    #         attachment_ids += tmpl.attachment_ids.ids
    #         description += (tmpl.description or '') + '\n'
    #         note += (tmpl.note or '') + '\n'
    #     self.attachment_ids = [(6, 0, attachment_ids)]
    #     self.description = description
    #     self.note = note

    @api.onchange('document_template_ids')
    def _onchange_document_template_id(self):
        attachment_ids = []
        description = note = ''
        attachment_papers = []
        attachment_papers_ids = []
        for tmpl in self.document_template_ids:
            attachment_ids += tmpl.attachment_ids.ids
            description += (tmpl.description or '') + '\n'
            note += (tmpl.note or '') + '\n'
            for attachment_paper in tmpl.attachment_papers:
                if attachment_paper.id in attachment_papers:
                    continue
                attachment_papers.append(attachment_paper.id)
                attachment_papers_ids.append(
                    (0, 0, {
                        'attachment_papers_id': attachment_paper.id,
                        'name': attachment_paper.name,
                    })
                )
        self.attachment_ids = [(6, 0, attachment_ids)]
        self.description = description
        self.note = note
        self.attachment_papers_ids = attachment_papers_ids

    @api.multi
    def action_confirm(self):
        self.state = 'awaiting_approval'
        self.send_email_and_sms()
        # if len(self.attachment_ids_2) != 0:
        #     self.state = 'awaiting_approval'
        #     self.send_email_and_sms()
        # else:
        #     raise UserError(_("Attach file is none"))

    @api.multi
    def action_approval(self):
        self.state = 'approved'
        self.send_email_and_sms()

    @api.multi
    def action_re_work(self):
        self.state = 'rework'
        self.send_email_and_sms()

    @api.multi
    def action_vn_post_done(self):
        for rec in self:
            if rec.document_send_type == 'direct':
                rec.state = 'done'
            else:
                rec.state = 'vn_post_done'
                rec.date_vn_post_send = date.today()

    @api.multi
    def action_money_received(self):
        self.payment = True
        self.env.ref('bms_cpdt.payment_email_templates').send_mail(self.id)
        self.env.ref('bms_cpdt.money_received_sms_templates').send_sms(self.id)

        if self.profile_received:
            self.state = "vn_post_check"
            self.send_email_and_sms()

    def action_mark_received_document(self):
        self.profile_received = True
        self.env.ref('bms_cpdt.profile_received_email_templates') \
            .send_mail(self.id)
        self.env.ref('bms_cpdt.profile_received_sms_templates') \
            .send_sms(self.id)

        if self.payment:
            self.state = "vn_post_check"
            self.send_email_and_sms()

    @api.multi
    def action_check_profile_document(self):
        self.state = 'vn_post_check'
        self.send_email_and_sms()

    @api.multi
    def action_missing_profile(self):
        self.state = 'missing_profile'
        self.profile_received = False
        # self.payment = False
        self.send_email_and_sms()

    @api.multi
    def action_result_profile_sent(self):
        self.state = 'result_profile_sent'
        self.send_email_and_sms()

    @api.multi
    def action_result_profile_returned(self):
        self.state = 'result_profile_returned'
        self.send_email_and_sms()

    @api.multi
    def action_mark_lost_document(self):
        self.state = 'vn_post_lost'
        self.profile_received = False
        self.payment = False
        self.send_email_and_sms()

    @api.multi
    def action_mark_done(self):
        self.state = 'done'
        self.send_email_and_sms()

    @api.multi
    def action_mark_close(self):
        self.state = 'close'
        self.send_email_and_sms()

    def action_mark_cancel(self):
        self.state = 'cancel'

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
        url = '/payment_info/%s' % self.id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    @api.multi
    def sms_action(self):
        self.ensure_one()
        return {
            'name': 'SMS Compose',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bms.sms.compose',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_to_number': self.mobile,
                'default_session_id': self.id,
            }
        }


class BMSSessionProduct(models.Model):
    _name = 'bms.session.product'

    @api.multi
    @api.depends('quantity', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.quantity
            line.price_subtotal_tax = line.price_subtotal * line.tax / 100

    @api.multi
    @api.depends('product_id')
    def _compute_get_price_unit(self):
        for r in self:
            r.price_unit = r.product_id.lst_price
            r.code = r.product_id.default_code

    name = fields.Char(string='Seal content')
    sequence = fields.Integer()
    product_id = fields.Many2one('product.product', string='Seal type')
    quantity = fields.Float()
    code = fields.Char(compute='_compute_get_price_unit', store=True)
    price_unit = fields.Float(compute='_compute_get_price_unit', store=True)
    tax = fields.Float()
    price_subtotal = fields.Float(compute='_compute_amount', store=True)
    price_subtotal_tax = fields.Float(compute='_compute_amount', store=True)
    session_id = fields.Many2one('bms.session', string='Session',
                                 ondelete='cascade')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            # self.name = self.product_id.name
            self.quantity = 1


class BMSSessionAttachment(models.Model):
    _name = 'bms.session.attachment'
    _inherits = {'ir.attachment': 'attachment_id'}
    _description = 'Bms Session Attachment'

    attachment_papers_id = fields.Many2one('bms.papers.template',
                                           string='Attachment',
                                           required=True, ondelete='cascade')
    session_id = fields.Many2one('bms.session',
                                 required=True, ondelete='cascade')
    paper_datas = fields.Binary(related='attachment_papers_id.datas',
                                string='Template File',
                                readonly=True)
    paper_datas_fname = fields.Char(related='attachment_papers_id.datas_fname',
                                    string='Template File name',
                                    readonly=True)
    user_attachment_ids = fields.Many2many(
        'ir.attachment', 'session_attachment_attachment_rel',
        'sesion_id', 'attachment_id',
        string='User attachments')
