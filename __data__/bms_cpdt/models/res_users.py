# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import api, exceptions, models
from odoo.tools.translate import _

p = '^\+?\d{1,3}?[- .]?\(?(?:\d{2,3})\)?[- .]?\d\d\d[- .]?\d\d\d\d$'


class Users(models.Model):
    _inherit = 'res.users'

    @api.multi
    @api.constrains('mobile')
    def _check_phone_number(self):
        for rec in self:
            if rec.mobile and not re.match(p, rec.mobile):
                raise exceptions.ValidationError(_(
                    'The mobile number is not available'))
        return True

    @api.model
    def set_home_action(self):
        is_manager = self.has_group('bms_cpdt.group_e_gov_manager')
        if is_manager:
            action_id = self.env.ref('bms_cpdt.action_session_form').id
            self.env.cr.execute(
                'update res_users set action_id =%s where id =%s',
                [action_id, self.id])
            return True

        is_user = self.has_group('bms_cpdt.group_e_gov_user')
        if is_user:
            action_id = self.env.ref(
                'bms_cpdt.wizard_bms_wellcome_action_form').id
            self.env.cr.execute(
                'update res_users set action_id =%s where id =%s',
                [action_id, self.id])
        return True

    @api.model
    def create(self, vals):
        user = super(Users, self).create(vals)
        user.set_home_action()
        return user

    @api.multi
    def write(self, vals):
        res = super(Users, self).write(vals)
        if not vals.get('action_id', False):
            self.set_home_action()
        return res
