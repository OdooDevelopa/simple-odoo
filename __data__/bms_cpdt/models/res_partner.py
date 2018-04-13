# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import api, exceptions, models, fields
from odoo.tools.translate import _

p = '^\+?\d{1,3}?[- .]?\(?(?:\d{2,3})\)?[- .]?\d\d\d[- .]?\d\d\d\d$'


class ResPartner(models.Model):
    _inherit = 'res.partner'

    identification_number = fields.Char(string="The identification number")
    provide_by = fields.Char(string="Provided by")
    provide_date = fields.Char(string="Date provide")
    organization_name = fields.Char(string="Organization's name")
    organization_address = fields.Char(string="Organization's address")

    @api.model
    def signup_retrieve_info(self, token):
        res = super(ResPartner, self).signup_retrieve_info(token)
        partner = self._signup_retrieve_partner(token, raise_exception=True)
        if partner.mobile:
            res['mobile'] = partner.mobile
        if partner.identification_number:
            res['identification_number'] = partner.identification_number
        if partner.provide_by:
            res['provide_by'] = partner.provide_by
        if partner.provide_date:
            res['provide_date'] = partner.provide_date
        if partner.organization_name:
            res['organization_name'] = partner.organization_name
        if partner.organization_address:
            res['organization_address'] = partner.organization_address
        return res

    @api.multi
    @api.constrains('mobile')
    def _check_phone_number(self):
        for rec in self:
            if rec.mobile and not re.match(p, rec.mobile):
                raise exceptions.ValidationError(_(
                    'The mobile number is not available'))
        return True
