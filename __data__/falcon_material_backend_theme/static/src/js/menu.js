odoo.define('web.backend_falcon_theme', function(require) {
    "use strict";

    var core = require('web.core');
    var session = require('web.session');
    var Menu = require('web.Menu');
    var web_client = require('web.web_client');

    $(document).ready(function() {
        $('.o_sub_menu').prepend("<span class='si-icons'><span></span><span class='s2'></span><span></span></spn>");

        $('.o_sub_menu span.si-icons').click(
            function(e) {
                e.preventDefault(); // prevent the default action
                e.stopPropagation(); // stop the click from bubbling
                $('body').toggleClass('oe_leftbar_open');
            });
    });
});