# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class BaseConfiguration(models.TransientModel):
    """ Inherit the base settings to add favicon. """
    _inherit = 'base.config.settings'

    fav_icon_backend = fields.Binary('Favicon')
    backend_logo = fields.Binary('Logo')

    @api.multi
    def get_default_alias_domain(self, fields):
        fav_icon_backend = self.env["ir.config_parameter"].get_param(
            "fav_icon_backend", default=None)
        backend_logo = self.env["ir.config_parameter"].get_param("backend_logo", default=None)
        return {'fav_icon_backend': fav_icon_backend or False, 'backend_logo': backend_logo or False}

    @api.multi
    def set_alias_domain(self):
        for record in self:
            self.env['ir.config_parameter'].set_param(
                "fav_icon_backend", record.fav_icon_backend or '')
            self.env['ir.config_parameter'].set_param('backend_logo', record.backend_logo or '')
