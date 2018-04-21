# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class BMSReportRegister(models.Model):
    _name = "bms.report.register"
    _order = 'name desc'
    _auto = False

    name = fields.Char(string='User', readonly=True)
    register_date = fields.Date(string='Register Date', readonly=True)
    nbr_users = fields.Integer('# of Users', readonly=True)

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr_users,
                    u.id as id,
                    date(u.create_date) as register_date,
                    u.login as name
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    u.id,
                    register_date,
                    name
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM res_users u
                WHERE u.active = 'true' and u.create_date is not NULL
                %s
        """ % (self._table, self._select(), self._group_by()))
