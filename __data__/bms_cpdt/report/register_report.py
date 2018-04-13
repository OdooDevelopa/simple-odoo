# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class BMSReportRegister(models.Model):
    _name = "bms.report.register"
    _order = 'name desc'
    _auto = False

    name = fields.Char(string='User', readonly=True)
    register_date = fields.Date(readonly=True)
    nbr_users = fields.Integer('# of Users', readonly=True)

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
            "CREATE or REPLACE view bms_report_register as "
            "SELECT"
            "(select 1 ) AS nbr_users,"
            "u.id as id,"
            "date(u.create_date) as register_date,"
            "u.login as name "
            "FROM res_users u "
            "WHERE u.active = 'true' and u.create_date is not NULL "
            "GROUP BY u.id, register_date, name")
