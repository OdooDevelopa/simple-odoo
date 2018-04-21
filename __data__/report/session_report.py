# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class BMSReportSession(models.Model):
    _name = "bms.report.session"
    _order = 'name desc, user_id'
    _auto = False

    name = fields.Char(string='Session Title', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    document_template_id = fields.Many2one(
        'bms.document.template', string='Document Tempalte', readonly=True)
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
         ('cancel', 'Cancel')], string='State', readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True)
    document_send_type = fields.Selection(
        [('direct', 'Direct'),
         ('vn_post', 'VN Post')], string='Document Send Type', readonly=True)
    date_vn_post_send = fields.Date(string='Date VN Post Send')

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr_sessions,
                    s.id as id,
                    s.date as date,
                    s.date_vn_post_send as date_vn_post_send,
                    s.user_id,
                    s.name as name,
                    s.company_id,
                    s.state as state,
                    s.document_send_type as document_send_type,
                    s.document_template_id as document_template_id
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    s.id,
                    date,
                    date_vn_post_send,
                    s.user_id,
                    s.document_template_id,
                    s.document_send_type,
                    name,
                    s.company_id,
                    s.state
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM bms_session s
                %s
        """ % (self._table, self._select(), self._group_by()))
