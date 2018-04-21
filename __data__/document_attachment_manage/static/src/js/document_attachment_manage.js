odoo.define('document_attachment_manage', function (require) {
"use strict";

var core = require('web.core');
var Sidebar = require('web.Sidebar');

var _t = core._t;

Sidebar.include({
    start : function(){
        var self = this;
        self._super.apply(self, arguments);
        self.$el.on('click','.o_sidebar_manage_attachment', function(evt) {
            self.do_action({
                name: _t('Attachment Management'),
                type: 'ir.actions.act_window',
                res_model: 'ir.attachment',
                domain: [
                    '&',
                    ['res_model', '=', self.dataset.model],
                    ['res_id', '=', self.model_id]
                ],
                view_mode: 'tree,form',
                view_type: 'form',
                views: [
                    [false, 'list'],
                    [false, 'form']
                ],
                context: {
                    'default_res_model': self.dataset.model,
                    'default_res_id': self.model_id
                }
            });
            evt.preventDefault();
        });
    }
});

});