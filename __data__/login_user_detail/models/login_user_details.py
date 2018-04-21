# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2016-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Saritha Sahadevan(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################
import logging
from itertools import chain
from datetime import datetime
from odoo.http import request
from odoo import models, fields, api

_logger = logging.getLogger(__name__)
USER_PRIVATE_FIELDS = ['password']
concat = chain.from_iterable


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def check_credentials(self, password):
        result = super(ResUsers, self).check_credentials(password)
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        session_id = request.session.sid
        vals = {'name': self.name,
                'ip_address': ip_address,
                'session_id': session_id
                }
        self.env['login.detail'].sudo().create(vals)
        return result


class LoginUpdate(models.Model):
    _name = 'login.detail'

    name = fields.Char(string="User Name")
    date_time = fields.Datetime(string="Login Date And Time",
                                default=datetime.now())
    sign_out = fields.Datetime(string="Sign Out Date")
    ip_address = fields.Char(string="IP Address")
    session_id = fields.Char(string="Session ID")
