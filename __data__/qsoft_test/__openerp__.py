# -*- encoding: utf-8 -*-
##############################################################################
#
#    Samples module for QSoft
#    Copyright (C) 2017- Serenco JSC (http://www.serenco.net)
#    @author: MinhHQ (minh.hq@serenco.net)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Source: https://docs.google.com/document/d/1SLu5YMxs0TCu2qHLf0ENOuwswVl7bCR91J4XmOJiTzE/edit
#
##############################################################################
{
    'name': 'QSoft Test',
    'summary': 'Odoo Developer Test',
    'version': '1.0',
    'category': 'QSoft Modules',
    'author': 'minh.hq (minh.hq@serenco.net)',
    'website': 'http://www.serenco.net',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        # ====== Wizard ======== #
        'wizard/share_profile.xml',

        # ====== Views ========= #
        'views/res_partner_view.xml',
        'views/mail_template.xml',
        'views/report_mapping.xml',

        # ====== Reports ======= #
        'reports/share_profile_template.xml'
    ],
    'installable': True,
}
