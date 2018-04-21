# -*- coding: utf-8 -*-
###############################################################################
#
#    Serenco JSC, Open Source Management Solution
#    Copyright (C) 2006 Serenco JSC (<http://serenco.net>). All Rights Reserved
#    @author: Minh.HQ <minh.hq@serenco.net>
#
###############################################################################

import logging
from openerp import api, tools, models, fields, _
import openerp.modules

_logger = logging.getLogger(__name__)


class SerencoVietnamTranslate(models.TransientModel):
    _name = "serenco.vietnam.translate"

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    @api.multi
    def act_translate(self):
        _logger.info('act_translate() BEGIN')
        self.env.cr.execute("delete from ir_translation where module in ('document','mail')")
        self.env.cr.commit
        module_rcs = self.env['ir.module.module'].search([('name','in',('document','mail'))])
        # module_rcs = self.pool['ir.module.module'].browse([])
        modules = [m.name for m in module_rcs if m.state in ('installed', 'to install', 'to upgrade')]
        for module_name in modules:
            trans_file = openerp.modules.get_module_resource('serenco_translation_vietnam', 'i18n', module_name + '.po')
            if trans_file:
                _logger.info('module %s: loading translation file (%s) for language %s', module_name, 'vi_VN', 'vi_VN')
                tools.trans_load(self._cr, trans_file, 'vi_VN', verbose=False, module_name=module_name)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
