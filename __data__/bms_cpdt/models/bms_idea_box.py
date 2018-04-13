# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class BMSIdeaBox(models.Model):
    _name = 'bms.idea.box'
    _inherit = ['mail.thread']
    _description = 'Bms idea box'
    _rec_name = 'id'

    session_id = fields.Many2one('bms.session', string='Session',
                                 required=True, readonly=True)
    content = fields.Text('Idea content', required=True, readonly=True,
                          states={'draft': [('readonly', False)]})
    ranking = fields.Selection([('0-none', 'None ranking'),
                                ('1-bad', 'Bad'),
                                ('2-mendium', 'Mendium'),
                                ('3-good', 'Good')],
                               default='0-none', readonly=True,
                               states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                             ('processing', 'Processing'),
                             ('done', 'Done'),
                             ('cancel', 'Cancel')],
                             required=True, readonly=True,
                             default='draft')

    @api.multi
    def action_processing(self):
        for idea in self:
            if idea.state == 'draft':
                idea.write({'state': 'processing'})
        return True

    @api.multi
    def action_done(self):
        for idea in self:
            if idea.state == 'processing':
                idea.write({'state': 'done'})
        return True

    @api.multi
    def action_cancel(self):
        user_flag = self.env.user.has_group('bms_cpdt.group_e_gov_user')
        manager_flag = self.env.user.has_group('bms_cpdt.group_e_gov_manager')
        for idea in self:
            if idea.state == 'draft' and user_flag:
                idea.write({'state': 'cancel'})
            elif idea.state in ('draft', 'processing') and manager_flag:
                idea.write({'state': 'cancel'})
        return True

    @api.multi
    def unlink(self):
        for idea in self:
            if idea.state != 'cancel':
                raise UserError(_(
                    'Error: '
                    'You only can delete cancel idea!'))
        return super(BMSIdeaBox, self).unlink()

    def save(self):
        return True
