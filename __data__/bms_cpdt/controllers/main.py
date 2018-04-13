# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.tools.translate import _


class LegalBasic(http.Controller):
    @http.route('/LegalBasic/<int:id>/', auth='public', website=True)
    def LegalBasicId(self, id):
        Legal_basics = http.request.env['bms.legal.basic']
        return http.request.render('bms_cpdt.LegalBasicId', {
            'legal_basics': Legal_basics.search([
                ('id', '=', id),
            ])
        })

    @http.route('/co-so-phap-ly/', auth='public', website=True)
    def index(self, **kw):
        LegalBasic = http.request.env['bms.legal.basic']
        return http.request.render('bms_cpdt.LegalBasic', {
            'LegalBasic': LegalBasic.sudo().search([])
        })


class Home(http.Controller):
    @http.route('/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('bms_cpdt.homepage_inherit', {})


class AdministrativeProcedures(http.Controller):
    @http.route('/dang-ky-quan-ly-con-dau/', auth='public', website=True)
    def dang_ky_quan_ly_con_dau(self, **kw):
        # Document_template_categ = http.request.env[
        #     'bms.document.template.category']
        # dtc1 = Document_template_categ.env.ref('bms_cpdt.dtc1').id
        return http.request.render('bms_cpdt.AdministrativeProceduresCateg',
                                   {})

    @http.route('/thu-tuc-lam-con-dau-moi/',
                auth='public', website=True)
    def thu_tuc_lam_con_dau_moi(self, **kw):
        return http.request.render('bms_cpdt.thu_tuc_lam_con_dau_moi',
                                   {})

    @http.route('/thu-tuc-lam-con-dau-noi-dau-thu-nho-dau-xi/',
                auth='public', website=True)
    def thu_tuc_lam_con_dau_noi_dau_thu_nho_dau_xi(self, **kw):
        return http.request.render(
            'bms_cpdt.thu_tuc_lam_con_dau_noi_dau_thu_nho_dau_xi',
            {})

    @http.route('/thu-tuc-dang-ky-lai-mau-con-dau/',
                auth='public', website=True)
    def thu_tuc_dang_ky_lai_mau_con_dau(self, **kw):
        return http.request.render('bms_cpdt.thu_tuc_dang_ky_lai_mau_con_dau',
                                   {})

    @http.route('/thu-tuc-lam-them-con-dau/', auth='public', website=True)
    def thu_tuc_lam_them_con_dau(self, **kw):
        return http.request.render('bms_cpdt.thu_tuc_lam_them_con_dau',
                                   {})

    @http.route('/thu-tuc-cap-doi-cap-lai-'
                'giay-chung-nhan-da-dang-ky-mau-con-dau/',
                auth='public', website=True)
    def thu_tuc_cap_doi_cap_lai_giay_chung_nhan_da_dang_ky_mau_con_dau(
            self, **kw):
        return http.request.render('bms_cpdt.thu_tuc_cap_doi_cap_lai_'
                                   'giay_chung_nhan_da_dang_ky_mau_con_dau',
                                   {})

    # @http.route('/AdministrativeProceduresCateg/<int:catg_id>',
    #             auth='public', website=True)
    # def AdministrativeProceduresCategId(self, catg_id):
    #     Document_template_categ = \
    #         http.request.env['bms.document.template.category']
    #     return http.request.render(
    # 'bms_cpdt.AdministrativeProceduresCateg', {
    #         'categs': Document_template_categ.sudo().search([]),
    #         'current_catge': Document_template_categ.sudo().browse(catg_id),
    #     })

    @http.route('/AdministrativeProcedures/', auth='public', website=True)
    def AdministrativeProcedures(self, **kw):
        Document_templates = http.request.env['bms.document.template']
        return http.request.render('bms_cpdt.AdministrativeProcedures', {
            'document_templates': Document_templates.sudo().search([])
        })

    @http.route('/AdministrativeProcedures/<int:id>/',
                auth='public', website=True)
    def AdministrativeProceduresId(self, id):
        Document_templates = http.request.env['bms.document.template']
        return http.request.render('bms_cpdt.AdministrativeProceduresId', {
            'document_templates': Document_templates.sudo().search([
                ('id', '=', id),
            ])
        })

    @http.route('/.well-known/pki-validation/fileauth.txt', type='http', auth='public',
                website=True)
    def ssl_validate(self):
        key = http.request.env['ir.config_parameter'].sudo().get_param(
            'ssl_auth',
            default='y698xw3dvch14d6ctv79f234zql2qhht')
        return key

class PaymentInfo(http.Controller):
    @http.route('/payment_info/<int:session_id>', type='http', auth='public',
                website=True)
    def render_payment_info_page(self, session_id):
        sessions = http.request.env['bms.session'].sudo().browse(session_id)
        return http.request.render('bms_cpdt.payment_info', {
            'sessions': sessions
        })

    @http.route('/payment_success/<int:session_id>', type='http',
                auth='public', website=True)
    def render_payment_success(self, session_id):
        sessions = http.request.env['bms.session'].sudo().browse(session_id)
        return http.request.render('bms_cpdt.payment_success', {
            'sessions': sessions
        })

    @http.route('/payment_error/<int:session_id>', type='http', auth='public',
                website=True)
    def render_payment_error(self, session_id):
        sessions = http.request.env['bms.session'].sudo().browse(session_id)
        return http.request.render('bms_cpdt.payment_error', {
            'sessions': sessions
        })


class PasswordSecurityHome(AuthSignupHome):
    def do_signup(self, qcontext):
        assert qcontext.get('password') == qcontext.get('confirm_password'), _(
            "Passwords do not match; please retype them.")
        return super(PasswordSecurityHome, self).do_signup(qcontext)
