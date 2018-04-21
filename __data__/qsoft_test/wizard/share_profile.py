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
#
##############################################################################

import re
import base64

from openerp import api, fields, models, _
from openerp.exceptions import UserError
import time


class ShareProfile(models.TransientModel):
    _name = 'share.profile'
    _description = 'Share Profile'

    name = fields.Char(string='Title', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    datas_fname = fields.Char(string='File Name')
    email_from = fields.Char(string='From:', required=True)
    email_to = fields.Char(string='To:', required=True)
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
    datas = fields.Binary(string='Datas')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)

    @api.model
    def default_get(self, fields):
        context = dict(self._context or {})
        res = super(ShareProfile, self).default_get(fields)
        res_partner_obj = self.env['res.partner']
        partner_id = res_partner_obj.browse(context.get('active_id'))
        datas = self.get_file_pdf(partner_id)
        datas_fname = 'QSoftTest_' + partner_id.name + '_Profile.pdf'
        res.update({'email_from': partner_id.email,
                    'partner_id': partner_id.id,
                    'datas_fname': datas_fname,
                    'datas': datas})
        return res

    @api.multi
    def get_file_pdf(self, partner_id):
        ir_actions_report = self.env['ir.actions.report.xml']
        matching_reports = ir_actions_report.search([('name', '=', 'Share Profile')])
        if matching_reports:
            service = matching_reports.report_name
            # Render Share Profile PDF report
            # result, format = self.pool['report'].get_pdf(
            #     self._cr, self._uid, [partner_id.id], service, context=dict(self._context or {})), 'pdf'
            result, format = self.env['report'].get_pdf(partner_id.ids, service, data=None), 'pdf'
            eval_context = {'time': time, 'object': self}
            if not matching_reports.attachment or not eval(matching_reports.attachment, eval_context):
                result = base64.b64encode(result)
        return result

    @api.onchange('email_to')
    def validate_email(self):
        for rec in self:
            if rec.email_to:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", rec.email_to) != None:
                    pass
                else:
                    raise UserError(_("Please enter a valid email address"))

    @api.multi
    def send(self):
        self.ensure_one()
        attachment_obj = self.env['ir.attachment']

        # Find the e-mail template
        template = self.env.ref('qsoft_test.share_profile_email_template')

        # Send out the e-mail template to the user
        mail_temp_id = self.env['mail.template'].browse(template.id).send_mail(self.id)

        # Attachment file to e-mail waiting outgoing
        mail_id = self.env['mail.mail'].browse(mail_temp_id)
        file_name = re.sub(r'[^a-zA-Z0-9_-]', '_', 'Share Profile of:%s' % self.partner_id.name)
        file_name += ".pdf"
        attachment_id = attachment_obj.create(
            {
                'name': file_name,
                'datas': self.datas,
                'datas_fname': file_name,
                'res_model': self.partner_id._name,
                'res_id': self.partner_id.id,
                'type': 'binary'
            })
        mail_id.write({'attachment_ids': [(6, 0, [attachment_id.id])]})

        # Send e-mail now
        # mail_id.sent()

        # Delete attachment file on database
        # self.env['ir.attachment'].browse(attachment_id.id).unlink()

        return True
