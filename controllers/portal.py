# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import io

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website_sale.controllers.main import WebsiteSaleForm
from odoo.addons.website_membership.controllers.main import WebsiteMembership
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools.mimetypes import guess_mimetype


class PortalABVOCertificates(CustomerPortal):

    def _prepare_portal_layout_values(self):
        cert_user = False
        values = super(PortalABVOCertificates, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        # cert_count = partner.certificates_lines
        cert_count = len(partner.search([('boat_owner_id', '=', partner.id)]).mapped('certificates_lines'))

        # if partner.user_id and not partner.user_id._is_public():
        #     cert_user = partner.user_id

        values.update(
            {'cert_count': cert_count})
        return values
        # return {
        #     'sales_user': cert_user,
        #     'page_name': 'home',
        #     'archive_groups': [],
        #     # 'certificates_count': cert_count
        # }

    # ------------------------------------------------------------
    # My Invoices
    # ------------------------------------------------------------

    def _certificate_get_page_view_values(self, certificate, access_token, **kwargs):
        values = {
            'page_name': 'certificate',
            'invoice': certificate,
        }
        return self._get_page_view_values(certificate, access_token, values, 'my_certificates_history', False, **kwargs)

    @http.route(['/my/certificates', '/my/certificates/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_certificates(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        # AbvoCertificate = request.env['res.partner'].certificates_lines
        AbvoCertificate = partner.search([('boat_owner_id', '=', partner.id)]).mapped('certificates_lines')


        domain = []

        # searchbar_sortings = {
        #     'date': {'label': _('Invoice Date'), 'order': 'date_invoice desc'},
        #     'duedate': {'label': _('Due Date'), 'order': 'date_due desc'},
        #     'name': {'label': _('Reference'), 'order': 'name desc'},
        #     'state': {'label': _('Status'), 'order': 'state'},
        # }
        # # default sort by order
        if not sortby:
            sortby = 'date'
        # order = searchbar_sortings[sortby]['order']

        # archive_groups = self._get_archive_groups('account.invoice', domain)
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        # cert_count = AbvoCertificate.search_count(domain)
        cert_count = values.get('cert_count', 0)
        # pager
        pager = portal_pager(
            url="/my/certificates",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=cert_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        # certificates = AbvoCertificate.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        certificates = AbvoCertificate.search(domain, limit=self._items_per_page, offset=pager['offset'])
        # request.session['my_invoices_history'] = invoices.ids[:100]

        values.update({
            'date': date_begin,
            'certificates': certificates,
            'page_name': 'certificate',
            'pager': pager,
            # 'archive_groups': archive_groups,
            'default_url': '/my/certificates',
            # 'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("abvo.portal_my_certificates", values)

    # @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    # def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
    #     try:
    #         invoice_sudo = self._document_check_access('account.invoice', invoice_id, access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')

    #     if report_type in ('html', 'pdf', 'text'):
    #         return self._show_report(model=invoice_sudo, report_type=report_type, report_ref='account.account_invoices', download=download)

    #     values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
    #     PaymentProcessing.remove_payment_transaction(invoice_sudo.transaction_ids)
    #     return request.render("account.portal_invoice_page", values)

    @http.route(['/my/home/certificates/<int:cert_id>/pdf'], type='http', auth="user", website=True)
    def get_certification_pdf(self, cert_id):
        pdfname = "test"
        cert_obj = request.env['abvo.certificates'].sudo().browse(cert_id)
        cert_pdf = cert_obj.pdf
        pdf_base64 = base64.b64decode(cert_pdf)
        pdf_data = io.BytesIO(pdf_base64)
        mimetype = guess_mimetype(pdf_base64, default='application/pdf')
        pdfext = '.' + mimetype.split('/')[1]
        return http.send_file(pdf_data, filename=pdfname + pdfext, mimetype=mimetype, mtime=cert_obj.write_date)


class CustomWebsiteSaleFormAbvo(WebsiteSaleForm):

    @http.route('/website_form/shop.sale.order', type='http', auth="public", methods=['POST'], website=True)
    def website_form_saleorder(self, **post):

        boat_name = post.get('name')
        boat_id = None

        if post.get('boat_id'):
            boat_id = post.get('boat_id')
        elif boat_name:
            boat_id = request.env['res.partner'].sudo().create({
                'name': boat_name,
                'estaleiro': post.get('estaleiro'),
                'modelo': post.get('modelo'),
                'loa': post.get('loa'),
                'deslocamento': post.get('deslocamento'),
                'numeral': post.get('numeral'),
                'club_id': post.get('club_id'),
                'boat_owner_id': request.env.user.partner_id.id,
                'is_boat': True,
            })
            boat_id = boat_id.id

        if boat_id:
            order = request.website.sale_get_order()
            order.sudo().write({'boat_id': boat_id})
        return super(CustomWebsiteSaleFormAbvo, self).website_form_saleorder(**post)


class AbvoWebsiteMembership(WebsiteMembership):

    @staticmethod
    def _sort_members_set_by_name(members_set):
        return request.env['res.partner'].browse(members_set).sorted('name').ids

    def _sort_and_filter_members(self, members=None):
        if members:
            for m_line, partners in members.items():
                members.update({m_line: self._sort_members_set_by_name(set(partners))})
        return members

    @http.route([
        '/members',
        '/members/page/<int:page>',
        '/members/association/<membership_id>',
        '/members/association/<membership_id>/page/<int:page>',

        '/members/country/<int:country_id>',
        '/members/country/<country_name>-<int:country_id>',
        '/members/country/<int:country_id>/page/<int:page>',
        '/members/country/<country_name>-<int:country_id>/page/<int:page>',

        '/members/association/<membership_id>/country/<country_name>-<int:country_id>',
        '/members/association/<membership_id>/country/<int:country_id>',
        '/members/association/<membership_id>/country/<country_name>-<int:country_id>/page/<int:page>',
        '/members/association/<membership_id>/country/<int:country_id>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def members(self, membership_id=None, country_name=None, country_id=0, page=1, **post):
        res = super(AbvoWebsiteMembership, self).members(membership_id, country_name, country_id, page, **post)
        memberships_partner_ids = res.qcontext.get('memberships_partner_ids')
        res.qcontext.update(
            {'memberships_partner_ids': self._sort_and_filter_members(
                memberships_partner_ids)}
        )
        return res
