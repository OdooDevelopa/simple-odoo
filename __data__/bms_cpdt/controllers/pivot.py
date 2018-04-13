# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo import _
from odoo.addons.web.controllers.pivot import TableExporter


class BMSTableExporter(TableExporter):

    @http.route('/web/pivot/export_xls', type='http', auth="user")
    def export_xls(self, data, token):
        response = super(BMSTableExporter, self).export_xls(data, token)

        response.headers[1] = ('Content-Disposition',
                               _('attachment; filename=table.xls;'
                                 ).encode('utf-8'))

        return response
