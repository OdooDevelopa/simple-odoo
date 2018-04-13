# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class BMSReportSession(models.Model):
    _name = "bms.report.session"
    _order = 'name desc, user_id'
    _auto = False

    name = fields.Char(string='Session Title', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    date = fields.Date(readonly=True)
    # document_template_id = fields.Many2one(
    #     'bms.document.template', string='Document Tempalte', readonly=True)
    nbr_sessions = fields.Integer('# of Sessions', readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('awaiting_approval', 'Awaiting Approval'),
         ('rework', 'Re-Work'),
         ('approved', 'Approved'),
         ('vn_post', 'VN Post'),
         ('done', 'Done'),
         ('vn_post_lost', 'VN Post Lost'),
         ('vn_post_done', 'VN Post Done'),
         ('close', 'Close'),
         ('cancel', 'Cancel')], readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True)
    document_send_type = fields.Selection(
        [('direct', 'Direct'),
         ('vn_post', 'VN Post')], readonly=True)
    date_vn_post_send = fields.Date(string='Date VN Post Send')

    def _select(self):
        select_str = """
        """
        return select_str

    def _group_by(self):
        group_by_str = """
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            "CREATE or REPLACE view bms_report_session as "
            "SELECT"
            "(select 1 ) AS nbr_sessions,"
            "s.id as id,"
            "s.date as date,"
            "s.date_vn_post_send as date_vn_post_send,"
            "s.user_id,"
            "s.name as name,"
            "s.company_id,"
            "s.state as state,"
            "s.document_send_type as document_send_type "
            "FROM bms_session s "
            "GROUP BY s.id, date, date_vn_post_send, s.user_id, "
            "s.document_send_type, name, s.company_id, s.state")
