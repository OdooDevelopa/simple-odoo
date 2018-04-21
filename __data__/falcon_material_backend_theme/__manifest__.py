
# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Falcon Material Backend Theme',
    'description': 'Customizable Backend Theme Based on Material Design',
    'summary':'Customizable Backend Theme Based on Material Design',
    'category': 'Theme/Backend',
    'version': '10.0.1.0.0',
    'author': 'AppJetty',
    'website': 'https://goo.gl/rAuut4',
    'support': 'support@appjetty.com',
    'depends': ['web','product'],
    'data': [
             'views/template.xml', 
             'views/base_config_view.xml',
             'views/ir_ui_menu_view.xml',
             'views/assets.xml',
    ],
    'installable': True,
    'qweb': ['static/src/xml/base.xml'],
    'application': True,
    'live_test_url': 'http://theme-falcon-material.appjetty.com',
    'images': ['static/description/splash-screen.png'],
    'price': 119.00,
    'currency': 'EUR',
}
