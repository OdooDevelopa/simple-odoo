# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BmsWellcome(models.Model):
    _name = 'bms.wellcome'
    _description = 'Bms wellcome'

    state = fields.Selection([('choose', 'choose'),
                              ('new', 'new'),
                              ('follow', 'Follow'),
                              ],
                             compute='_compute_state')

    @api.model
    def _compute_state(self):
        ctx = dict(self.env.context) or {}
        state = ctx.get('state', 'choose')
        for w in self:
            w.state = state

    def show_action(self):
        action = self.env.ref(
            'bms_cpdt.wizard_bms_wellcome_action_form')
        res = action.read()
        return res[0]

    def new_registration_procedure(self):
        res = self.show_action()
        res['context'] = {'state': 'new'}
        return res

    def follow(self):
        res = self.show_action()
        res['context'] = {'state': 'follow'}
        return res

    def back(self):
        res = self.show_action()
        res['context'] = {'state': 'choose'}
        return res

    def open_url(self, model, type, action_id):
        url = '/web?#view_type={}&model={}&action={}'.format(
            type, model, action_id)
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': url,
        }

    def new_set_calendar(self):
        action = self.env.ref(
            'bms_cpdt.bms_set_calendar_action_form')[0]
        return self.open_url('bms.set.calendar', 'form', action.id)

    def new_send_a_copy(self):
        action = self.env.ref(
            'bms_cpdt.action_session_send_a_copy_form')[0]
        return self.open_url('bms.session', 'form', action.id)

    def new_session(self):
        action = self.env.ref(
            'bms_cpdt.action_view_my_session')[0]
        return self.open_url('bms.session', 'form', action.id)

    def follow_set_calendar(self):
        action = self.env.ref(
            'bms_cpdt.bms_set_calendar_action_form')[0]
        return self.open_url('bms.set.calendar', 'tree', action.id)

    def follow_send_a_copy(self):
        action = self.env.ref(
            'bms_cpdt.action_session_send_a_copy_form')[0]
        return self.open_url('bms.session', 'tree', action.id)

    def follow_session(self):
        action = self.env.ref(
            'bms_cpdt.action_view_my_session')[0]
        return self.open_url('bms.session', 'tree', action.id)
