# -*- coding: utf-8 -*-
# Copyright (C) 2006 Serenco JSC (<http://serenco.net>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'BMS CPDT',
    'version': '10.0.1.0.0',
    'author': 'OpenERP SA, MONK Software, Odoo Community Association (OCA)',
    'category': 'BMS Modules',
    'license': 'AGPL-3',
    'website': 'https://odoo-community.org/',
    'depends': [
        'base',
        'mail',
        'login_user_detail',
        'product',
    ],
    'data': [
        'data/day_warning_miss_document.xml',
        'data/session_sequence.xml',
        'security/e_gov_security.xml',
        'security/ir.model.access.csv',
        'views/bms_document_template_views.xml',
        'views/bms_session_views.xml',
        'report/session_report_view.xml',
        'report/register_report_view.xml',
        'views/bms_document_menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
