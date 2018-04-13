# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from datetime import datetime
import pytz
from datetime import timedelta
from odoo.exceptions import UserError


class BMSSetCalendar(models.Model):
    _name = 'bms.set.calendar'
    _inherit = ['mail.thread']
    _description = 'Set calendar'
    _rec_name = 'date'
    _order = 'date'

    date = fields.Datetime(required=True, track_visibility='onchange',
                           readonly=True, string='Reception date time',
                           states={'draft': [('readonly', False)],
                                   'change': [('readonly', False)]})
    date_format = fields.Char(compute='_compute_date_format',
                              store=False)
    content = fields.Html(string='Work content', required=True,
                          track_visibility='onchange',
                          readonly=True,
                          states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'propose'),
                              ('confirm', 'Officials confirm'),
                              ('change', 'Officials change date'),
                              ('done', 'Both agreed'),
                              ('cancel', 'Cancel')
                              ], required=True, default='draft',
                             track_visibility='onchange', readonly=True)
    document_template_ids = fields.Many2many(
        'bms.document.template', 'bms_set_calendar_document_template_rel',
        'set_calendar_id', 'document_template_id',
        string='The document template I want to do',
        readonly=True,
        states={'draft': [('readonly', False)]})
    create_uid = fields.Many2one('res.users', 'Create by')
    date_editable = fields.Boolean(compute='_compute_date_editable',
                                   default=True)

    @api.multi
    def _compute_date_editable(self):
        is_user = self.env.user.has_group('bms_cpdt.group_e_gov_user')
        is_manager = self.env.user.has_group('bms_cpdt.group_e_gov_manager')
        for set_calendar in self:
            set_calendar.date_editable = False
            if set_calendar.state in ('draft', 'change') and is_manager:
                set_calendar.date_editable = True
                continue
            if set_calendar.state == 'draft' and is_user:
                set_calendar.date_editable = True

    @api.model
    def check_date(self):
        now = datetime.now()
        for set_calendar in self:
            date = set_calendar.date
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if date < now:
                raise UserError(_(
                    'Error: '
                    'You cannot set appointment time less than now!'))

    @api.model
    def create(self, vals):
        res = super(BMSSetCalendar, self).create(vals)
        res.check_date()
        return res

    @api.multi
    def write(self, vals):
        res = super(BMSSetCalendar, self).write(vals)
        self.check_date()
        return res

    @api.multi
    def change_utc_to_local_datetime(self, souce_date):
        user_tz = self.env.user.tz or str(pytz.utc)
        tz_now = datetime.now(pytz.timezone(user_tz))
        difference = tz_now.utcoffset().total_seconds() / 60 / 60
        difference = int(difference)
        utc_date = datetime.strptime(souce_date,
                                     '%Y-%m-%d %H:%M:%S')
        utc_date = utc_date + timedelta(hours=difference)
        return utc_date.strftime('%Y-%m-%d %H:%M:%S')

    @api.multi
    @api.depends('date')
    def _compute_date_format(self):
        for set_calendar in self:
            date_format = set_calendar.date
            date_format = self.change_utc_to_local_datetime(date_format)
            date_format = datetime.strptime(
                date_format,
                '%Y-%m-%d %H:%M:%S')
            date_format = date_format.strftime('%H:%M:%S  %d-%m-%Y')
            set_calendar.date_format = date_format

    def confirm(self):
        if self.state == 'draft':
            self.write({'state': 'confirm'})
        return True

    def send_mail_change(self):
        template = self.env.ref(
            'bms_cpdt.set_calendar_change_date_email_templates')
        # self.env['mail.template'].browse(template.id).send_mail(self.id)
        mail_id = template.send_mail(self.id)
        # self.env['mail.mail'].browse(mail_id).send()
        try:
            self.env['mail.mail'].browse(mail_id).send()
        except Exception:
            return True
        return True

    def change(self):
        if self.state == 'draft':
            self.write({'state': 'change'})
            self.send_mail_change()
        return True

    def cancel(self):
        if self.state not in ('done', 'cancel'):
            self.write({'state': 'cancel'})
        return True

    def done(self):
        if self.state in ('change', 'confirm'):
            self.write({'state': 'done'})
        return True
