# -*- coding: utf-8 -*-

import logging

from openerp import api, fields, models, _

_logger = logging.getLogger(__name__)

CONFIG_PARAM_WEB_WINDOW_TITLE = "web.base.title"

class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    web_window_title = fields.Char('Window Title')

    @api.model
    def get_default_web_window_title(self, fields):
        ir_config = self.env['ir.config_parameter']
        web_window_title = ir_config.get_param(CONFIG_PARAM_WEB_WINDOW_TITLE, "")
        return dict(web_window_title=web_window_title)

    @api.multi
    def set_default_web_window_title(self):
        self.ensure_one()
        ir_config = self.env['ir.config_parameter']
        web_window_title = self.web_window_title or ""
        ir_config.set_param(CONFIG_PARAM_WEB_WINDOW_TITLE, web_window_title)
        return True
