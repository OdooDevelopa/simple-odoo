# -*- coding: utf-8 -*-
# Copyright (C) 2006 BMS Group Global (<http://www.bmsgroupglobal.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Department(models.Model):

    _inherit = "hr.department"

    tel_number = fields.Char(string='Telephone number')
    bms_document_tmpl_ids = fields.One2many(
        'bms.document.template', 'department_id', string='Document Template')
